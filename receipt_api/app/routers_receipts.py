from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from .auth import get_db, get_current_user
from .models import Receipt, ReceiptItem
from .schemas import ReceiptCreate, ReceiptOut

router = APIRouter()

@router.post("/", response_model=ReceiptOut)
def create_receipt(data: ReceiptCreate,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    new_receipt = Receipt(
        user_id=current_user.id,
        payment_type=data.payment.type,
        payment_amount=data.payment.amount,
        receipt_link=str(uuid.uuid4())
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)

    total_amount = 0
    items_out = []
    for prod in data.products:
        item_total = float(prod.price) * float(prod.quantity)
        total_amount += item_total
        receipt_item = ReceiptItem(
            receipt_id=new_receipt.id,
            name=prod.name,
            price=prod.price,
            quantity=prod.quantity,
            total=item_total
        )
        db.add(receipt_item)
        items_out.append({
            "name": prod.name,
            "price": float(prod.price),
            "quantity": float(prod.quantity),
            "total": item_total
        })

    db.commit()
    db.refresh(new_receipt)

    new_receipt.total = total_amount
    db.commit()
    db.refresh(new_receipt)

    rest = 0
    if data.payment.type == "cash":
        rest = float(data.payment.amount) - total_amount

    return ReceiptOut(
        id=new_receipt.id,
        products=items_out,
        payment={"type": data.payment.type, "amount": float(data.payment.amount)},
        total=float(new_receipt.total),
        rest=rest,
        created_at=str(new_receipt.created_at)
    )

@router.get("/")
def get_receipts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_total: Optional[float] = None,
    max_total: Optional[float] = None,
    payment_type: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = db.query(Receipt).filter(Receipt.user_id == current_user.id)

    if date_from:
        query = query.filter(Receipt.created_at >= date_from)
    if date_to:
        query = query.filter(Receipt.created_at <= date_to)
    if min_total is not None:
        query = query.filter(Receipt.total >= min_total)
    if max_total is not None:
        query = query.filter(Receipt.total <= max_total)
    if payment_type:
        query = query.filter(Receipt.payment_type == payment_type)

    receipts = query.order_by(Receipt.id.desc()).offset(offset).limit(limit).all()
    return receipts

@router.get("/{receipt_id}")
def get_receipt_by_id(receipt_id: int,
                      db: Session = Depends(get_db),
                      current_user=Depends(get_current_user)):
    receipt = db.query(Receipt).filter(
        Receipt.id == receipt_id,
        Receipt.user_id == current_user.id
    ).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found.")
    return receipt

@router.get("/public/{receipt_link}")
def get_receipt_public_view(receipt_link: str,
                            db: Session = Depends(get_db),
                            width: int = 32):
    receipt = db.query(Receipt).filter(Receipt.receipt_link == receipt_link).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found.")

    lines = []
    lines.append("      ФОП Джонсонюк Борис       ".center(width))
    lines.append("=" * width)
    for item in receipt.items:
        line = f"{float(item.quantity)} x {float(item.price)} {float(item.total)}"
        lines.append(line[:width])
        lines.append(item.name[:width])
        lines.append("-" * width)
    lines.append(("СУМА " + str(float(receipt.total))).rjust(width))
    pay_line = (receipt.payment_type + " " + str(float(receipt.payment_amount))).rjust(width)
    lines.append(pay_line)
    rest = 0
    if receipt.payment_type == "cash":
        rest = float(receipt.payment_amount) - float(receipt.total)
    lines.append(("Решта " + str(rest)).rjust(width))
    lines.append("=" * width)
    date_str = receipt.created_at.strftime("%d.%m.%Y %H:%M")
    lines.append(date_str.center(width))
    lines.append("Дякуємо за покупку!".center(width))

    return {"receipt_text": "\n".join(lines)}
