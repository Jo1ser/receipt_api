from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers_users import router as user_router
from .routers_receipts import router as receipt_router

app = FastAPI(title="Receipt API")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API is up and running"}

app.include_router(user_router, prefix="/auth", tags=["Users"])
app.include_router(receipt_router, prefix="/receipts", tags=["Receipts"])
