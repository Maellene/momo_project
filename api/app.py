from fastapi import FastAPI

app = FastAPI(title="MoMo SMS Serialization API")

@app.get("/api/database-test")
def test_database():
    return {
        "status": "ok",
        "message": "Database schema ready for MoMo SMS processing",
        "entities": ["users", "transactions", "categories", "system_logs"]
    }

@app.get("/api/schema/user")
def user_schema():
    return {
        "id": "integer",
        "name": "string",
        "phone_number": "string",
        "created_at": "datetime"
    }

@app.get("/api/schema/category")
def category_schema():
    return {
        "category_id": "integer",
        "name": "string",
        "description": "string"
    }

@app.get("/api/schema/transaction")
def transaction_schema():
    return {
        "transaction_id": "integer",
        "amount": "decimal",
        "currency": "string",
        "transaction_type": "string",
        "timestamp": "datetime",
        "user": {
            "user_id": "integer",
            "name": "string",
            "phone_number": "string"
        },
        "category": {
            "category_id": "integer",
            "name": "string"
        }
    }



@app.get("/api/example/transaction")
def example_transaction():
    return {
        "transaction_id": 45821,
        "amount": 15000.50,
        "currency": "RWF",
        "transaction_type": "PAYMENT",
        "timestamp": "2026-01-20T14:32:10",
        "user": {
            "user_id": 12,
            "name": "Alice Mukamana",
            "phone_number": "0781234567"
        },
        "category": {
            "category_id": 3,
            "name": "Utilities"
        },
        "system_log": {
            "status": "SUCCESS",
            "processed_at": "2026-01-20T14:32:12",
            "message": "Transaction processed successfully"
        }
    }
