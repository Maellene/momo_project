# MoMo SMS REST API Documentation

## Overview
The MoMo SMS REST API provides secure access to mobile money transaction data. This API allows clients to create, read, update, and delete SMS transaction records.

**Base URL:** `http://localhost:8000`

**Authentication:** Basic Authentication (username/password)

---

## Authentication

All API endpoints require Basic Authentication.

**Credentials:**
- Username: `admin`
- Password: `momo2024`

**Header Format:**
```
Authorization: Basic YWRtaW46bW9tbzIwMjQ=
```

**Example (curl):**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions
```

---

## Endpoints

### 1. List All Transactions

Get a list of all SMS transactions in the system.

**Endpoint:** `GET /transactions`

**Authentication:** Required

**Request Example:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions
```

**Success Response (200 OK):**
```json
{
  "count": 22,
  "transactions": [
    {
      "id": 1,
      "type": "DEPOSIT",
      "amount": 50000.0,
      "sender": "250788123456",
      "receiver": "MOMO_AGENT_001",
      "timestamp": "2024-01-15T10:30:00",
      "status": "COMPLETED",
      "fee": 500.0
    },
    {
      "id": 2,
      "type": "WITHDRAWAL",
      "amount": 30000.0,
      "sender": "250788234567",
      "receiver": "MOMO_AGENT_002",
      "timestamp": "2024-01-15T11:45:00",
      "status": "COMPLETED",
      "fee": 300.0
    }
  ]
}
```

**Error Responses:**

| Status Code | Description | Response |
|------------|-------------|----------|
| 401 | Unauthorized | `{"error": "Unauthorized - Invalid or missing credentials", "status_code": 401}` |

---

### 2. Get Transaction by ID

Retrieve a specific transaction by its ID.

**Endpoint:** `GET /transactions/{id}`

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Transaction ID

**Request Example:**
```bash
curl -u admin:momo2024 http://localhost:8000/transactions/5
```

**Success Response (200 OK):**
```json
{
  "id": 5,
  "type": "PAYMENT",
  "amount": 25000.0,
  "sender": "250788567890",
  "receiver": "MERCHANT_001",
  "timestamp": "2024-01-16T10:30:00",
  "status": "COMPLETED",
  "fee": 250.0
}
```

**Error Responses:**

| Status Code | Description | Response |
|------------|-------------|----------|
| 400 | Invalid ID format | `{"error": "Invalid transaction ID - must be an integer", "status_code": 400}` |
| 401 | Unauthorized | `{"error": "Unauthorized - Invalid or missing credentials", "status_code": 401}` |
| 404 | Transaction not found | `{"error": "Transaction with ID 999 not found", "status_code": 404}` |

---

### 3. Create New Transaction

Add a new transaction to the system.

**Endpoint:** `POST /transactions`

**Authentication:** Required

**Request Headers:**
```
Content-Type: application/json
Authorization: Basic YWRtaW46bW9tbzIwMjQ=
```

**Request Body:**
```json
{
  "type": "TRANSFER",
  "amount": 15000,
  "sender": "250788123456",
  "receiver": "250788987654",
  "status": "COMPLETED",
  "fee": 150
}
```

**Required Fields:**
- `type` (string) - One of: DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT
- `amount` (number) - Transaction amount (must be > 0)
- `sender` (string) - Sender phone number or ID
- `receiver` (string) - Receiver phone number or ID

**Optional Fields:**
- `status` (string) - Default: "COMPLETED"
- `fee` (number) - Default: 1% of amount
- `timestamp` (string) - Default: current timestamp

**Request Example:**
```bash
curl -u admin:momo2024 -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TRANSFER",
    "amount": 15000,
    "sender": "250788123456",
    "receiver": "250788987654"
  }' \
  http://localhost:8000/transactions
```

**Success Response (201 Created):**
```json
{
  "message": "Transaction created successfully",
  "transaction": {
    "id": 23,
    "type": "TRANSFER",
    "amount": 15000.0,
    "sender": "250788123456",
    "receiver": "250788987654",
    "timestamp": "2024-01-30T10:30:00",
    "status": "COMPLETED",
    "fee": 150.0
  }
}
```

**Error Responses:**

| Status Code | Description | Response |
|------------|-------------|----------|
| 400 | Missing required field | `{"error": "Missing required field: type", "status_code": 400}` |
| 400 | Invalid transaction type | `{"error": "Invalid transaction type. Must be one of: DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT", "status_code": 400}` |
| 400 | Invalid amount | `{"error": "Amount must be greater than 0", "status_code": 400}` |
| 400 | Invalid JSON | `{"error": "Invalid JSON in request body", "status_code": 400}` |
| 401 | Unauthorized | `{"error": "Unauthorized - Invalid or missing credentials", "status_code": 401}` |

---

### 4. Update Transaction

Update an existing transaction.

**Endpoint:** `PUT /transactions/{id}`

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Transaction ID

**Request Headers:**
```
Content-Type: application/json
Authorization: Basic YWRtaW46bW9tbzIwMjQ=
```

**Request Body:** (All fields optional)
```json
{
  "amount": 20000,
  "status": "PENDING",
  "fee": 200
}
```

**Request Example:**
```bash
curl -u admin:momo2024 -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 20000,
    "status": "PENDING"
  }' \
  http://localhost:8000/transactions/5
```

**Success Response (200 OK):**
```json
{
  "message": "Transaction updated successfully",
  "transaction": {
    "id": 5,
    "type": "PAYMENT",
    "amount": 20000.0,
    "sender": "250788567890",
    "receiver": "MERCHANT_001",
    "timestamp": "2024-01-16T10:30:00",
    "status": "PENDING",
    "fee": 250.0
  }
}
```

**Error Responses:**

| Status Code | Description | Response |
|------------|-------------|----------|
| 400 | Invalid ID format | `{"error": "Invalid transaction ID - must be an integer", "status_code": 400}` |
| 400 | Invalid data | `{"error": "Amount must be greater than 0", "status_code": 400}` |
| 401 | Unauthorized | `{"error": "Unauthorized - Invalid or missing credentials", "status_code": 401}` |
| 404 | Transaction not found | `{"error": "Transaction with ID 999 not found", "status_code": 404}` |

---

### 5. Delete Transaction

Delete a transaction from the system.

**Endpoint:** `DELETE /transactions/{id}`

**Authentication:** Required

**URL Parameters:**
- `id` (integer, required) - Transaction ID

**Request Example:**
```bash
curl -u admin:momo2024 -X DELETE http://localhost:8000/transactions/5
```

**Success Response (200 OK):**
```json
{
  "message": "Transaction 5 deleted successfully",
  "id": 5
}
```

**Error Responses:**

| Status Code | Description | Response |
|------------|-------------|----------|
| 400 | Invalid ID format | `{"error": "Invalid transaction ID - must be an integer", "status_code": 400}` |
| 401 | Unauthorized | `{"error": "Unauthorized - Invalid or missing credentials", "status_code": 401}` |
| 404 | Transaction not found | `{"error": "Transaction with ID 999 not found", "status_code": 404}` |

---

## Error Codes Summary

| Status Code | Meaning |
|------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input or malformed request |
| 401 | Unauthorized - Authentication required or failed |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server-side error |

---

## Transaction Data Model

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Auto-generated | Unique transaction identifier |
| type | string | Yes | Transaction type (DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT) |
| amount | number | Yes | Transaction amount (must be positive) |
| sender | string | Yes | Sender phone number or identifier |
| receiver | string | Yes | Receiver phone number or identifier |
| timestamp | string | Auto-generated | ISO 8601 timestamp |
| status | string | Default: COMPLETED | Transaction status |
| fee | number | Auto-calculated | Transaction fee (default 1% of amount) |

---

## Testing with Postman

### Setup
1. Create a new collection named "MoMo API"
2. Add Authorization:
   - Type: Basic Auth
   - Username: `admin`
   - Password: `momo2024`

### Test Scenarios

**Scenario 1: Get All Transactions**
- Method: GET
- URL: `http://localhost:8000/transactions`
- Expected: 200 OK with transaction list

**Scenario 2: Get Single Transaction**
- Method: GET
- URL: `http://localhost:8000/transactions/1`
- Expected: 200 OK with transaction object

**Scenario 3: Create Transaction**
- Method: POST
- URL: `http://localhost:8000/transactions`
- Body: 
```json
{
  "type": "DEPOSIT",
  "amount": 50000,
  "sender": "250788111222",
  "receiver": "MOMO_AGENT_001"
}
```
- Expected: 201 Created

**Scenario 4: Update Transaction**
- Method: PUT
- URL: `http://localhost:8000/transactions/1`
- Body:
```json
{
  "amount": 60000
}
```
- Expected: 200 OK

**Scenario 5: Delete Transaction**
- Method: DELETE
- URL: `http://localhost:8000/transactions/1`
- Expected: 200 OK

**Scenario 6: Unauthorized Request**
- Method: GET
- URL: `http://localhost:8000/transactions`
- Authorization: None or wrong credentials
- Expected: 401 Unauthorized

---

## Testing with cURL

```bash
# Get all transactions
curl -u admin:momo2024 http://localhost:8000/transactions

# Get single transaction
curl -u admin:momo2024 http://localhost:8000/transactions/1

# Create transaction
curl -u admin:momo2024 -X POST \
  -H "Content-Type: application/json" \
  -d '{"type":"DEPOSIT","amount":50000,"sender":"250788111222","receiver":"MOMO_AGENT_001"}' \
  http://localhost:8000/transactions

# Update transaction
curl -u admin:momo2024 -X PUT \
  -H "Content-Type: application/json" \
  -d '{"amount":60000}' \
  http://localhost:8000/transactions/1

# Delete transaction
curl -u admin:momo2024 -X DELETE http://localhost:8000/transactions/1

# Test unauthorized access
curl http://localhost:8000/transactions
```

---

## Security Notes

### Current Implementation: Basic Authentication

**How it works:**
- Client sends username:password encoded in Base64
- Server decodes and verifies credentials
- Credentials sent with every request

**Limitations:**
1. **Not Encrypted:** Credentials are only Base64 encoded, not encrypted
2. **Vulnerable to Interception:** Can be decoded by anyone intercepting the request
3. **No Token Expiration:** Credentials valid indefinitely
4. **Transmitted with Every Request:** Increases exposure risk
5. **No User Management:** Hardcoded credentials, no user database

### Recommended Alternatives

**1. JWT (JSON Web Tokens)**
- Stateless authentication
- Token-based with expiration
- Can include user claims/permissions
- More secure than Basic Auth

**2. OAuth 2.0**
- Industry standard for authorization
- Supports multiple grant types
- Third-party authentication
- Better for complex applications

**3. API Keys with HTTPS**
- Unique keys per client
- Can be revoked individually
- Must use HTTPS to encrypt

### Best Practices
- **Always use HTTPS** in production
- Implement **rate limiting** to prevent abuse
- Use **strong password hashing** (bcrypt, argon2)
- Implement **token refresh** mechanisms
- Add **request logging** for security auditing
- Consider **IP whitelisting** for additional security

---

## Support

For issues or questions:
- Check the GitHub repository
- Review test cases in `/tests` folder
- Examine screenshots in `/screenshots` folder
