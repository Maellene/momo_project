"""
MoMo SMS REST API Server
Handles GET requests for transaction data
Author: Person 2
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys

# Allow importing from dsa folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dsa.xml_parser import parse_xml_to_json


# -----------------------------
# In-memory transaction storage
# -----------------------------
class TransactionStore:
    def __init__(self):
        self.transactions = []

    def load_from_xml(self, xml_path):
        self.transactions = parse_xml_to_json(xml_path)

    def get_all(self):
        return self.transactions

    def get_by_id(self, trans_id):
        for transaction in self.transactions:
            if transaction["id"] == trans_id:
                return transaction
        return None


store = TransactionStore()


# -----------------------------
# API Request Handler
# -----------------------------
class APIHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        # GET /transactions
        if self.path == "/transactions":
            self.send_json({
                "count": len(store.get_all()),
                "transactions": store.get_all()
            })
            return

        # GET /transactions/{id}
        if self.path.startswith("/transactions/"):
            try:
                trans_id = int(self.path.split("/")[-1])
                transaction = store.get_by_id(trans_id)

                if transaction:
                    self.send_json(transaction)
                else:
                    self.send_json({"error": "Transaction not found"}, 404)

            except ValueError:
                self.send_json({"error": "Invalid transaction ID"}, 400)

            return

        self.send_json({"error": "Endpoint not found"}, 404)


# -----------------------------
# Run Server
# -----------------------------
def run_server():
    xml_path = os.path.join(os.path.dirname(__file__), "..", "modified_sms_v2.xml")
    store.load_from_xml(xml_path)

    server = HTTPServer(("localhost", 8000), APIHandler)
    print("Server running at http://localhost:8000")
    print("GET  /transactions")
    print("GET  /transactions/{id}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
