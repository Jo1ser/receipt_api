# Receipt API

A REST API for managing receipts with user registration, login, and receipt creation.

## Features

- Register and authorize users using JWT
- Create receipts (products, payment details, etc.)
- List and filter user’s receipts (by date, total, payment type)
- View single receipt by ID
- Publicly view receipts at a unique link

## Requirements

- Python 3.12+
- PostgreSQL
- FastAPI
- Uvicorn

## Installation and Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/example/receipt_api.git
   cd receipt_api

   ```

2. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Configure database and environment variables:

```
set DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/receipt_db
set SECRET_KEY=some_secret_key
```

5. Run migrations or let the app create tables automatically(Tables are auto-created on startup in main.py)

6. Launch the server(This starts the API at http://127.0.0.1:8000):

```
uvicorn receipt_api.app.main:app --reload
```

## Usage & Endpoints

1. Register a New User

- Endpoint: `POST /auth/register`
- JSON body:

```
{
  "username": "testuser",
  "password": "testpassword",
  "name": "Test User"
}
```

2. Login and Get Token

- Endpoint: `POST /auth/login`
- JSON body:

```
{
  "username": "testuser",
  "password": "testpassword"
}
```

3. Create a Receipt

- Endpoint: `POST /receipts/`
- Headers: `Authorization: Bearer <token>`
- JSON body example:

```
{
  "products": [
    {"name": "Product A", "price": 150.0, "quantity": 2}
  ],
  "payment": {"type": "cash", "amount": 500.0}
}
```

4. List Receipts

- Endpoint: `GET /receipts`
- Headers: `Authorization: Bearer <token>`
- Query parameters (optional):

```
date_from
date_to
min_total
max_total
payment_type
limit
offset
```

5. View Single Receipt:

- Endpoint: `GET /receipts/{receipt_id}`
- Headers: `Authorization: Bearer <token>`

6. View Public Receipt:
   Endpoint: `GET /receipts/public/{receipt_link}`

## Running Tests

Use pytest to run the tests:
`python -m pytest receipt_api/app/tests`
