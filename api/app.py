from fastapi import FastAPI

app = FastAPI(title="MoMo SMS Serialization API")

@app.get("/api/database-test")
def test_database():
    return {
        "status": "ok",
        "tables": [
            "users",
            "transactions",
            "categories",
            "user_transactions",
            "transaction_fees",
            "fee_types",
            "system_logs"
        ]
    }

@app.get("/api/schema/users")
def users_schema():
    return {
        "user_id": "integer",
        "phone_number": "string",
        "full_name": "string"
    }

@app.get("/api/schema/categories")
def categories_schema():
    return {
        "category_id": "integer",
        "category_name": "string",
        "category_type": "string",
        "description": "string"
    }

@app.get("/api/schema/transactions")
def transactions_schema():
    return {
        "transaction_id": "integer",
        "txn_code": "string",
        "amount": "decimal",
        "message": "string",
        "transaction_date": "datetime",
        "category_id": "integer"
    }



@app.get("/api/example/complete-transaction")
def complete_transaction_example():
    return {
        "transaction_id": 76662021700,
        "txn_code": "RCV",
        "amount": 2000,
        "message": "You have received money",
        "transaction_date": "2026-01-10 16:30:51",

        "category": {
            "category_id": 1,
            "category_name": "Received Money",
            "category_type": "Income"
        },

        "users": [
            {
                "user_id": 1,
                "full_name": "James Kundwa",
                "phone_number": "+250788123456",
                "role": "sender"
            },
            {
                "user_id": 2,
                "full_name": "Account Owner",
                "phone_number": "+25078XXXXXX",
                "role": "receiver"
            }
        ],

        "fees": [
            {
                "fee_type": "Transaction Fee",
                "fee_amount": 0
            }
        ],

        "system_log": {
            "message": "Transaction processed successfully",
            "date": "2026-01-10 16:30:52"
        }
    }
