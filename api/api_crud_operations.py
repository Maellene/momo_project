"""
API CRUD Operations - POST, PUT, DELETE
Handles create, update, and delete operations
"""

import json
from datetime import datetime


def validate_transaction_data(data, is_update=False):
    """
    Validate transaction data
    
    Args:
        data (dict): Transaction data to validate
        is_update (bool): Whether this is an update operation
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['type', 'amount', 'sender', 'receiver']
    
    # For updates, not all fields are required
    if not is_update:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    # Validate transaction type
    valid_types = ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT']
    if 'type' in data and data['type'] not in valid_types:
        return False, f"Invalid transaction type. Must be one of: {', '.join(valid_types)}"
    
    # Validate amount
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except (ValueError, TypeError):
            return False, "Amount must be a valid number"
    
    # Validate fee if provided
    if 'fee' in data:
        try:
            fee = float(data['fee'])
            if fee < 0:
                return False, "Fee cannot be negative"
        except (ValueError, TypeError):
            return False, "Fee must be a valid number"
    
    return True, None


def handle_post(handler, store):
    """
    Handle POST /transactions - Create new transaction
    
    Args:
        handler: HTTP request handler
        store: Transaction store
    """
    # Check authentication
    if not handler._check_authentication():
        handler._send_error_response(401, 'Unauthorized - Invalid or missing credentials')
        return
    
    try:
        # Read request body
        content_length = int(handler.headers.get('Content-Length', 0))
        post_data = handler.rfile.read(content_length)
        
        # Parse JSON
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            handler._send_error_response(400, 'Invalid JSON in request body')
            return
        
        # Validate data
        is_valid, error_msg = validate_transaction_data(data)
        if not is_valid:
            handler._send_error_response(400, error_msg)
            return
        
        # Set defaults for optional fields
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        if 'status' not in data:
            data['status'] = 'COMPLETED'
        
        if 'fee' not in data:
            # Calculate default fee (1% of amount)
            data['fee'] = round(float(data['amount']) * 0.01, 2)
        
        # Add transaction
        new_transaction = store.add(data)
        
        # Send response
        handler._send_json_response({
            'message': 'Transaction created successfully',
            'transaction': new_transaction
        }, 201)
    
    except Exception as e:
        handler._send_error_response(500, f'Internal server error: {str(e)}')


def handle_put(handler, store):
    """
    Handle PUT /transactions/{id} - Update existing transaction
    
    Args:
        handler: HTTP request handler
        store: Transaction store
    """
    # Check authentication
    if not handler._check_authentication():
        handler._send_error_response(401, 'Unauthorized - Invalid or missing credentials')
        return
    
    # Parse transaction ID from path
    path_parts = handler.path.split('/')
    
    if len(path_parts) < 3:
        handler._send_error_response(400, 'Transaction ID required in URL')
        return
    
    try:
        trans_id = int(path_parts[2])
    except ValueError:
        handler._send_error_response(400, 'Invalid transaction ID - must be an integer')
        return
    
    try:
        # Read request body
        content_length = int(handler.headers.get('Content-Length', 0))
        put_data = handler.rfile.read(content_length)
        
        # Parse JSON
        try:
            data = json.loads(put_data.decode('utf-8'))
        except json.JSONDecodeError:
            handler._send_error_response(400, 'Invalid JSON in request body')
            return
        
        # Validate data (partial validation for updates)
        is_valid, error_msg = validate_transaction_data(data, is_update=True)
        if not is_valid:
            handler._send_error_response(400, error_msg)
            return
        
        # Update transaction
        updated_transaction = store.update(trans_id, data)
        
        if updated_transaction:
            handler._send_json_response({
                'message': 'Transaction updated successfully',
                'transaction': updated_transaction
            })
        else:
            handler._send_error_response(404, f'Transaction with ID {trans_id} not found')
    
    except Exception as e:
        handler._send_error_response(500, f'Internal server error: {str(e)}')


def handle_delete(handler, store):
    """
    Handle DELETE /transactions/{id} - Delete transaction
    
    Args:
        handler: HTTP request handler
        store: Transaction store
    """
    # Check authentication
    if not handler._check_authentication():
        handler._send_error_response(401, 'Unauthorized - Invalid or missing credentials')
        return
    
    # Parse transaction ID from path
    path_parts = handler.path.split('/')
    
    if len(path_parts) < 3:
        handler._send_error_response(400, 'Transaction ID required in URL')
        return
    
    try:
        trans_id = int(path_parts[2])
    except ValueError:
        handler._send_error_response(400, 'Invalid transaction ID - must be an integer')
        return
    
    try:
        # Delete transaction
        success = store.delete(trans_id)
        
        if success:
            handler._send_json_response({
                'message': f'Transaction {trans_id} deleted successfully',
                'id': trans_id
            })
        else:
            handler._send_error_response(404, f'Transaction with ID {trans_id} not found')
    
    except Exception as e:
        handler._send_error_response(500, f'Internal server error: {str(e)}')


# Authentication utilities
def create_auth_header(username, password):
    """
    Create Basic Auth header for testing
    
    Args:
        username (str): Username
        password (str): Password
        
    Returns:
        str: Authorization header value
    """
    import base64
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


if __name__ == '__main__':
    # Test authentication header creation
    print("Testing Authentication Header Generation")
    print("=" * 50)
    
    # Valid credentials
    valid_header = create_auth_header('admin', 'momo2024')
    print(f"Valid credentials header:")
    print(f"  Authorization: {valid_header}")
    
    # Invalid credentials
    invalid_header = create_auth_header('user', 'wrong')
    print(f"\nInvalid credentials header:")
    print(f"  Authorization: {invalid_header}")
    
    print("\n" + "=" * 50)
    print("Use these headers in your HTTP requests!")
    print("\nExample curl command:")
    print(f'curl -H "Authorization: {valid_header}" http://localhost:8000/transactions')
