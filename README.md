# momo_project

WEBCORE TEAMMATES

- Benjamin Niyomurinzi 
- Alia Nirere Sayinzoga
- Noella Uwera
- Maellene Mpinganzima
---
## Project Description
This project is an enterprise-level full-stack application that processes Mobile Money (MoMo) SMS data provided in XML format.  

The system extracts, cleans, categorizes, and stores transaction data in a relational database, then provides analytics and visualizations through a web-based dashboard.

The goal is to help users understand their mobile money transaction history, spending patterns, and income sources using structured data processing and visualization.

---
## System Architecture

The system follows a pipeline-based architecture:

1. **XML File (Input)**  
   Raw MoMo SMS data provided in XML format.

2. **ETL Pipeline (Python Scripts)**  
   - Parse XML messages  
   - Clean and normalize data (amounts, dates, phone numbers)  
   - Categorize transactions (incoming, outgoing, payments, transfers)

3. **SQLite Database**  
   Stores cleaned and structured transaction data.

4. **REST API (FastAPI)**  
   Provides endpoints to access transactions and analytics.

5. **Web Dashboard**  
   Displays transaction summaries, charts, and tables using HTML, CSS, and JavaScript.
## Architecture diagram link address :
https://github.com/Maellene/momo_project/blob/main/webcore%20momo%20project.png

---
## Scrum Board :
We are using a Scrum board to manage tasks and collaborate using Agile practices.                                                                                                                                                 
https://github.com/users/Maellene/projects/3/views/1
---

## Week 2: Database Design & Implementation

**Team participation sheet:** [https://docs.google.com/spreadsheets/d/1v9yugnSn8R4a8Q26f_xiZw5wrP991b7TCrbwRVfN7pU/edit?usp=sharing]

### Entity Relationship Diagram (ERD)

Our database consists of **7 tables** designed to handle MoMo SMS transaction processing with proper normalization and referential integrity.

![Database ERD](https://github.com/Maellene/momo_project/blob/main/docs/erd_diagram.pdf)

**Core Tables:**
- **users** - Customer accounts and profiles
- **transactions** - Main transaction records
- **categories** - Transaction type classification
- **user_transactions** - User participation mapping (sender/receiver roles)

**Supporting Tables:**
- **fee_types** - Fee definitions and calculation rules
- **transaction_fees** - Junction table resolving M:N relationship between transactions and fees
- **system_logs** - ETL process tracking and monitoring


---

### Database Schema Overview
![Database Design Document](https://github.com/Maellene/momo_project/blob/main/docs/Database%20Design%20Document%20WebCores.pdf)

#### Key Relationships

1. **categories → transactions** (1:M)
   - One category can have many transactions
   - Each transaction belongs to one category

2. **users → user_transactions** (1:M)
   - One user can participate in many transactions
   - Each participation record belongs to one user

3. **transactions → user_transactions** (1:M)
   - One transaction can have multiple participants (sender + receiver)
   - Each participation record belongs to one transaction

4. **transactions ↔ fee_types** (M:N)  **Many-to-Many Relationship**
   - One transaction can have multiple fees (transaction fee + tax + service charge)
   - One fee type can apply to multiple transactions
   - Resolved through **transaction_fees** junction table

5. **system_logs** (Standalone)
   - Independent logging table for ETL monitoring

#### Database Features

 **Many-to-Many Relationship:** Transactions ↔ Fee Types (via transaction_fees junction table)  
 **Referential Integrity:** Foreign key constraints prevent orphaned records  
 **Data Validation:** CHECK constraints ensure positive amounts and valid balances  
 **Duplicate Prevention:** UNIQUE constraints on phone numbers and transaction codes  
 **Performance Optimization:** Strategic indexes on frequently queried columns  
 **Audit Trail:** Timestamp tracking on all tables  
 **Controlled Deletion:** RESTRICT for critical data, CASCADE for dependent details

---

### Database Setup

see [View datadase Query we used](https://github.com/Maellene/momo_project/blob/main/database/database_setup.sql) for more information

#### Prerequisites
- MySQL 8.0 or higher
- Python 3.8+
- pip (Python package manager)

#### Installation Steps

1. **Install MySQL** (if not already installed)
```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server

   # macOS
   brew install mysql
   brew services start mysql
```

2. **Run Database Setup Script**
```bash
   mysql -u momo_user -p momo_db < database/database_setup.sql
```

3. **Verify Installation**
```bash
   mysql -u momo_user -p momo_db -e "SHOW TABLES;"
```

   Expected output: 7 tables (users, categories, transactions, user_transactions, fee_types, transaction_fees, system_logs)

---

### JSON Data Examples

Our database data can be serialized to JSON for API responses:

#### Simple User Object
```json
{
  "user_id": 1,
  "phone_number": "+250788123456",
  "full_name": "KAMANZI Ghod",
  "email": "kamanzi@example.com",
  "account_status": "active",
  "registration_date": "2023-06-10T08:30:00Z"
}
```

#### Complete Transaction with Relationships (M:N Demonstrated)
```json
{
  "transaction_id": 1,
  "txn_code": "TXN001",
  "amount": 5000.00,
  "transaction_date": "2024-01-15T10:00:00Z",
  "status": "completed",
  "category": {
    "category_name": "Received Money",
    "category_type": "Income"
  },
  "sender": {
    "full_name": "UWIMANA Jane",
    "phone_number": "+250789654321"
  },
  "receiver": {
    "full_name": "KAMANZI Ghod",
    "phone_number": "+250788123456"
  },
  "fees": [
    {
      "fee_name": "Transaction Fee",
      "fee_amount": 75.00
    },
    {
      "fee_name": "Tax",
      "fee_amount": 25.00
    }
  ],
  "total_fees": 100.00,
  "total_cost": 5100.00
}
```

See [examples/json_schemas.json](https://github.com/Maellene/momo_project/blob/main/examples/json_schemas.json) for complete examples.

---


## Development Workflow

### Getting Started

1. **Clone the repository**
```bash
   git clone https://github.com/Maellene/momo_project.git
   cd momo_project
```

## Team Collaboration

### Scrum Board
We manage our project using Agile Scrum practices.

 **Scrum Board:** [View on GitHub Projects](https://github.com/users/Maellene/projects/3/views/1)


## Week 2 Deliverables

###  Completed
- [x] Entity Relationship Diagram (ERD) with 7 tables
- [x] Many-to-Many relationship resolved with junction table
- [x] Complete MySQL database schema with constraints
- [x] Sample data (5+ records per table)
- [x] JSON schema examples
- [x] Design rationale documentation (250-300 words)
- [x] Complete data dictionary
- [x] Sample queries demonstrating functionality
- [x] Security constraint testing with screenshots
- [x] Updated README with database documentation
- [x] Team participation sheet
- [x] Database Design Document (PDF)

### Repository Structure
```
✓ docs/erd_diagram.png
✓ docs/Database Design Document WebCores.pdf
✓ database/database_setup.sql
✓ examples/json_schemas.json
✓ README.md (this file)
```

---

## Documentation

see [Database Design Document](https://github.com/Maellene/momo_project/blob/main/docs/Database%20Design%20Document%20WebCores.pdf) for more information

### Key Documents
- **ERD Diagram:** [docs/erd_diagram.png](docs/erd_diagram.png)
- **Sample Queries:** [database/sample_queries.sql](https://github.com/Maellene/momo_project/blob/main/docs/Database%20Design%20Document%20WebCores.pdf)
- **JSON Examples:** [examples/json_schemas.json](examples/json_schemas.json)
- **Team participation sheet:** [https://docs.google.com/spreadsheets/d/1v9yugnSn8R4a8Q26f_xiZw5wrP991b7TCrbwRVfN7pU/edit?usp=sharing] 
- **AI Usage Log:** [docs/ai_usage_log.md](https://github.com/Maellene/momo_project/blob/main/examples/json_schemas.json)

### Database Design Highlights

**Many-to-Many Relationship:**
Transactions can have multiple fees, and fee types can apply to multiple transactions. This M:N relationship is resolved through the `transaction_fees` junction table, allowing flexible fee structures while maintaining data integrity.

**Security Features:**
- Foreign key constraints prevent orphaned records
- CHECK constraints enforce business rules (positive amounts)
- UNIQUE constraints prevent duplicates
- CASCADE/RESTRICT rules control deletion behavior

**Performance:**
- Strategic indexes on frequently queried columns
- Composite indexes for common query patterns
- Proper data types (DECIMAL for money, DATETIME for timestamps)

---

## Future Enhancements

### Planned Features
-  Real-time transaction processing
-  Advanced analytics dashboard
-  Mobile app integration
-  Multi-currency support
-  Machine learning for fraud detection
-  Automated report generation
-  Export functionality (PDF, Excel)
-  User authentication system

---

## AI Usage Transparency

### Policy Compliance

Our team has maintained full transparency regarding AI tool usage during this project. We have adhered to all permitted and prohibited use guidelines.

### Permitted Uses (What We Did)
- Grammar and spelling checks in documentation  
- SQL syntax verification for MySQL 8.0 compatibility  
- Research on MySQL indexing and constraint best practices  
- Formatting assistance for technical documentation 

### Prohibited Uses (What We Did NOT Do)
- AI did not generate our ERD design  
- AI did not create our database schema or relationships  
- AI did not write our business logic  
- AI did not create our design rationale or technical explanations

**All core design work - including ERD structure, table relationships, Many-to-Many resolution, constraint logic, and design rationale - was created by our team through collaborative analysis of MoMo transaction requirements.**

### Verification of Original Work

Our database design reflects genuine team understanding:
- ERD created in collaborative team session (January 22, 2-4 PM)
- Many-to-Many relationship identified through business analysis
- Junction table solution designed by the team
- All SQL schema and constraints written by team members
- Design rationale documents our actual decision-making process

Each team member can individually explain our design decisions, demonstrating authentic understanding rather than AI-generated solutions.

---

## Week 3: REST API Development & Security

**Team participation sheet:** [https://docs.google.com/spreadsheets/d/1zO08VvjfJKMarj71JbhSs9W7tdYTCmh-gheu2CMvzaQ/edit?usp=sharing]

### MoMo SMS REST API

A secure REST API for managing mobile money SMS transaction data, built with Python's `http.server` module.

### Features

 XML to JSON data parsing  
 RESTful API with CRUD operations  
 Basic Authentication  
 Data Structure & Algorithm comparison  
 Comprehensive API documentation  
 Automated testing suite  
 Manual test scripts (cURL & Postman)

### API Project Files

**Core API Files:**
- [api/api_server.py](api/api_server.py) - Main API server with GET endpoints
- [api/api_crud_operations.py](api/api_crud_operations.py) - POST/PUT/DELETE handlers

**Data Processing Files:**
- [dsa/xml_parser.py](dsa/xml_parser.py) - XML to JSON parser
- [dsa/search_comparison.py](dsa/search_comparison.py) - Algorithm performance comparison

**Documentation:**
- [docs/api_docs.md](docs/api_docs.md) - Complete API documentation


**Testing:**
- [tests/api_tests.py](tests/api_tests.py) - Automated test suite (8 tests)
- [SCREENSHOT of Test Cases](screenshots) - Testing and screenshot instructions

**Reports:**
- [MoMo_API_Project_Report.pdf](docs/MoMo_API_Project_Report.pdf) - Complete project report (PDF)


**Team Documents:**
- [https://docs.google.com/spreadsheets/d/1zO08VvjfJKMarj71JbhSs9W7tdYTCmh-gheu2CMvzaQ/edit?usp=sharing](TEAM_PARTICIPATION) - Team contribution template

**Data & Config:**
- [modified_sms_v2.xml](modified_sms_v2.xml) - Sample SMS transaction data (22 records)
- [requirements.txt](requirements.txt) - Python dependencies

### Project Structure for week 3

```
api/
├── api_server.py              # Main API server (GET endpoints)
└── api_crud_operations.py     # POST/PUT/DELETE handlers

dsa/
├── xml_parser.py              # XML parsing module
└── search_comparison.py       # Search algorithm comparison

docs/
└── api_docs.md                # Complete API documentation

tests/
└── api_tests.py               # Automated test suite

screenshots/                   # API test screenshots
modified_sms_v2.xml            # Sample transaction data
requirements.txt               # Python dependencies
```

### API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/transactions` | List all transactions | Yes |
| GET | `/transactions/{id}` | Get single transaction | Yes |
| POST | `/transactions` | Create new transaction | Yes |
| PUT | `/transactions/{id}` | Update transaction | Yes |
| DELETE | `/transactions/{id}` | Delete transaction | Yes |

### Quick Start

**1. Install Dependencies**
```bash
pip install requests
```

**2. Start the API Server**
```bash
cd api
python api_server.py
```

Server will start on `http://localhost:8000`

**Default Credentials:**
- Username: `admin`
- Password: `momo2024`

**3. Test the API**

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
```

**4. Run Automated Tests**
```bash
cd tests
python api_tests.py
```

**5. Run DSA Performance Comparison**
```bash
cd dsa
python search_comparison.py
```
![search_comparison1](https://github.com/user-attachments/assets/8bf6061f-d57f-4dc0-a677-6c039a380fe1)
![search_comparison2](https://github.com/user-attachments/assets/01bb107b-47fb-47bf-9c95-cbee81e5600e)
![search_comparision3](https://github.com/user-attachments/assets/205048d0-f120-484a-a3f7-277d269e9662)
![search_comparision4](https://github.com/user-attachments/assets/f054a865-bfd1-46d3-bdd5-1b40efd11ba2)

### Data Structures & Algorithms

The project implements and compares two search methods:

**Linear Search - O(n)**
- Sequentially scans through all records
- Time grows linearly with data size

**Dictionary Lookup - O(1)**
- Uses a hash table for direct access
- Constant time regardless of data size

**Performance Results:**
- Dictionary lookup is ~25x faster than linear search
- For 22 transactions: Dictionary averages 0.01μs vs Linear's 0.25μs
- Performance gap increases dramatically with more data

### Security

**Current Implementation: Basic Authentication**

**Limitations:**
- Credentials sent with every request
- Base64 encoding (not encryption)
- No token expiration
- Vulnerable to interception without HTTPS

**Recommended Improvements:**
1. Use HTTPS in production
2. Implement JWT for stateless authentication
3. Use OAuth 2.0 for third-party access
4. Hash passwords with bcrypt or argon2
5. Add rate limiting to prevent abuse
6. Implement API keys for client identification

### Testing

**Test Coverage:**
- GET all transactions (authenticated)
- GET all transactions (unauthorized)
- GET single transaction
- GET non-existent transaction
- POST create transaction
- POST invalid transaction
- PUT update transaction
- DELETE transaction

**Test Results:** 8/8 tests passing (100% success rate)

### Week 3 Deliverables

###  Completed
- [x] XML Parser (converts SMS data to JSON)
- [x] REST API with all 5 CRUD endpoints
- [x] Basic Authentication implementation
- [x] Data Structures & Algorithms comparison (Linear Search vs Dictionary)
- [x] Complete API documentation with examples
- [x] Automated test suite (8 tests, 100% pass rate)
- [x] Manual testing with cURL commands
- [x] Performance analysis and DSA report
- [x] Security analysis (Basic Auth limitations + alternatives)
- [x] Professional PDF report
- [x] Editable Word document report
- [x] Team participation sheet template
- [x] Quick start guide
- [x] Screenshot guide for testing
- [x] Git workflow documentation

### Repository Structure (Week 3 Addition)
```
✓ api/api_server.py
✓ api/api_crud_operations.py
✓ dsa/xml_parser.py
✓ dsa/search_comparison.py
✓ docs/api_docs.md
✓ tests/api_tests.py
✓ screenshots/ (to be added)
✓ MoMo_API_Project_Report.pdf
✓ MoMo_API_Project_Report.docx
✓ TEAM_PARTICIPATION_SHEET.md
✓ QUICK_START.md
✓ SCREENSHOT_GUIDE.md
✓ GIT_WORKFLOW.md
✓ PROJECT_SUMMARY.md
✓ DELIVERABLES_SUMMARY.md
✓ modified_sms_v2.xml
✓ requirements.txt
```

---
