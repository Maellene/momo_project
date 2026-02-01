"""
MoMo SMS REST API Server
Handles GET requests for transaction data
Author: Person 2
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import from dsa folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dsa.xml_parser import parse_xml_to_json


class TransactionStore:
    """In-memory storage for transactions"""
    
    def __init__(self):
        self.transactions = []
        self.transactions_dict = {}
        self.next_id = 1
    
    def load_from_xml(self, xml_path):
        """Load transactions from XML file"""
        self.transactions = parse_xml_to_json(xml_path)
        self.transactions_dict = {trans['id']: trans for trans in self.transactions}
        if self.transactions:
            self.next_id = max(trans['id'] for trans in self.transactions) + 1
    
    def get_all(self):
        """Get all transactions"""
        return self.transactions
    
    def get_by_id(self, trans_id):
        """Get transaction by ID"""
        return self.transactions_dict.get(trans_id)
    
    def add(self, transaction):
        """Add new transaction"""
        transaction['id'] = self.next_id
        self.next_id += 1
        self.transactions.append(transaction)
        self.transactions_dict[transaction['id']] = transaction
        return transaction
    
    def update(self, trans_id, updated_data):
        """Update existing transaction"""
        if trans_id not in self.transactions_dict:
            return None
        
        # Update the transaction
        transaction = self.transactions_dict[trans_id]
        for key, value in updated_data.items():
            if key != 'id':  # Don't allow ID changes
                transaction[key] = value
        
        return transaction
    
    def delete(self, trans_id):
        """Delete transaction"""
        if trans_id not in self.transactions_dict:
            return False
        
        # Remove from both list and dict
        transaction = self.transactions_dict[trans_id]
        self.transactions.remove(transaction)
        del self.transactions_dict[trans_id]
        
        return True


# Global transaction store
store = TransactionStore()


class APIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the API"""
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set response headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_error_response(self, status_code, message):
        """Send error response"""
        self._send_json_response({
            'error': message,
            'status_code': status_code
        }, status_code)
    
    def _check_authentication(self):
        """Check Basic Authentication"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            print("❌ Authentication failed: No Authorization header")
            return False
        
        try:
            # Basic Auth format: "Basic base64(username:password)"
            import base64
            auth_type, credentials = auth_header.split(' ', 1)
            
            if auth_type.lower() != 'basic':
                print("❌ Authentication failed: Not Basic Auth")
                return False
            
            # Decode credentials
            decoded = base64.b64decode(credentials).decode('utf-8')
            username, password = decoded.split(':', 1)
            
            # Check credentials (hardcoded for demo - INSECURE!)
            # In production, use hashed passwords and database
            VALID_USERNAME = 'admin'
            VALID_PASSWORD = 'momo2024'
            
            is_valid = (username == VALID_USERNAME and password == VALID_PASSWORD)
            
            if is_valid:
                print(f"✅ Authentication successful: {username}")
            else:
                print(f"❌ Authentication failed: Invalid credentials (username={username})")
            
            return is_valid
        
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self._set_headers(204)
    
    def do_GET(self):
        """Handle GET requests"""
        # Check authentication
        if not self._check_authentication():
            self._send_error_response(401, 'Unauthorized - Invalid or missing credentials')
            return
        
        # Parse path
        path_parts = self.path.split('/')
        
        # GET /transactions - List all transactions
        if self.path == '/transactions' or self.path == '/transactions/':
            transactions = store.get_all()
            self._send_json_response({
                'count': len(transactions),
                'transactions': transactions
            })
            return
        
        # GET /transactions/{id} - Get single transaction
        elif len(path_parts) >= 3 and path_parts[1] == 'transactions':
            try:
                trans_id = int(path_parts[2])
                transaction = store.get_by_id(trans_id)
                
                if transaction:
                    self._send_json_response(transaction)
                else:
                    self._send_error_response(404, f'Transaction with ID {trans_id} not found')
            
            except ValueError:
                self._send_error_response(400, 'Invalid transaction ID - must be an integer')
            return
        
        # Unknown endpoint
        else:
            self._send_error_response(404, 'Endpoint not found')
    
    def do_POST(self):
        """Handle POST requests - implemented by Person 3"""
        from api_crud_operations import handle_post
        handle_post(self, store)
    
    def do_PUT(self):
        """Handle PUT requests - implemented by Person 3"""
        from api_crud_operations import handle_put
        handle_put(self, store)
    
    def do_DELETE(self):
        """Handle DELETE requests - implemented by Person 3"""
        from api_crud_operations import handle_delete
        handle_delete(self, store)
    
    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    """Start the API server"""
    # Load data
    xml_path = os.path.join(os.path.dirname(__file__), '..', 'modified_sms_v2.xml')
    print(f"Loading data from {xml_path}...")
    store.load_from_xml(xml_path)
    print(f"Loaded {len(store.get_all())} transactions")
    
    # Start server
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    
    print(f"\n{'='*60}")
    print(f"MoMo SMS REST API Server")
    print(f"{'='*60}")
    print(f"Server running on http://localhost:{port}")
    print(f"\nAvailable endpoints:")
    print(f"  GET    /transactions      - List all transactions")
    print(f"  GET    /transactions/{{id}} - Get transaction by ID")
    print(f"  POST   /transactions      - Create new transaction")
    print(f"  PUT    /transactions/{{id}} - Update transaction")
    print(f"  DELETE /transactions/{{id}} - Delete transaction")
    print(f"\nAuthentication: Basic Auth")
    print(f"  Username: admin")
    print(f"  Password: momo2024")
    print(f"\nPress Ctrl+C to stop the server")
    print(f"{'='*60}\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
