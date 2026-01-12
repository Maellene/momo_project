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
