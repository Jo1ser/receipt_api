from fastapi.testclient import TestClient
from receipt_api.app.main import app
from receipt_api.app.database import engine
from receipt_api.app.models import Base

client = TestClient(app)

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    Base.metadata.drop_all(bind=engine)

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "name": "Test User"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_login_user():
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None
    return token

def test_create_receipt():
    token = test_login_user()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/receipts/", headers=headers, json={
        "products": [
            {"name": "Mavic 3T", "price": 298870.00, "quantity": 3.00}
        ],
        "payment": {"type": "cash", "amount": 1000000}
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_list_receipts():
    token = test_login_user()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/receipts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_view_single_receipt():
    token = test_login_user()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/receipts", headers=headers)
    receipt_id = response.json()[0]["id"]
    response = client.get(f"/receipts/{receipt_id}", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json()

def test_view_public_receipt():
    token = test_login_user()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/receipts", headers=headers)
    receipt_link = response.json()[0]["receipt_link"]
    response = client.get(f"/receipts/public/{receipt_link}")
    assert response.status_code == 200
    assert "ФОП Джонсонюк Борис" in response.text

def run_tests():
    test_register_user()
    test_create_receipt()
    test_list_receipts()
    test_view_single_receipt()
    test_view_public_receipt()

if __name__ == "__main__":
    run_tests()
