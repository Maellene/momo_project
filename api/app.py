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
        "category_id": "integer",
        "amount": "decimal",
        "transaction_date": "datetime",
        "message": "string"
    }


@app.get("/api/schema/fee-types")
def fee_types_schema():
    return {
        "fee_type_id": "integer",
        "fee_name": "string",
        "fee_code": "string",
        "calculation_method": "string",
        "fee_value": "decimal",
        "min_fee": "decimal",
        "max_fee": "decimal",
        "is_active": "boolean",
        "created_at": "datetime"
    }


@app.get("/api/example/complete-transaction")
def complete_transaction_example():
    return {
        "transaction": {
            "transaction_id": 1,
            "txn_code": "TXN001",
            "amount": 6000.00,
            "message": "Received money",
            "transaction_date": "2024-01-15 10:00:00",

            "category": {
                "category_id": 1,
                "category_name": "Received Money",
                "category_type": "Income",
                "description": "Incoming funds to wallet"
            },

            "users": [
                {
                    "user_id": 1,
                    "full_name": "NIZZA Oliver",
                    "phone_number": "+250788123456",
                    "role": "sender"
                },
                {
                    "user_id": 2,
                    "full_name": "UWARIYA Jane",
                    "phone_number": "+250789654321",
                    "role": "receiver"
                }
            ],

            "fees": [
                {
                    "transaction_fee_id": 1,
                    "fee_amount": 0.00,
                    "applied_at": "2024-01-15 10:00:01",
                    "fee_type": {
                        "fee_type_id": 1,
                        "fee_name": "Transaction Fee",
                        "fee_code": "TXN_FEE",
                        "calculation_method": "FIXED"
                    }
                }
            ],

            "system_log": {
                "id": 1,
                "message": "Transaction processed successfully",
                "date": "2024-01-15 10:00:01"
            }
        }
    }
