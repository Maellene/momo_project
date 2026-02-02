"""
XML Parser Module
Parses modified_sms_v2.xml and converts SMS records to JSON format
Extracts transaction information from SMS message bodies
"""

import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime


def extract_transaction_from_sms(sms_body, sms_data):
    """
    Extract transaction details from SMS message body.
    
    Args:
        sms_body (str): The SMS message text
        sms_data (dict): Raw SMS data from XML
        
    Returns:
        dict: Extracted transaction data or None if not a transaction
    """
    if not sms_body:
        return None
    
    transaction = {
        'address': sms_data.get('address'),
        'timestamp': sms_data.get('date'),
        'readable_date': sms_data.get('readable_date'),
        'body': sms_body,
        'message': sms_body,
        'status': sms_data.get('status'),
        'read': sms_data.get('read'),
        'service_center': sms_data.get('service_center')
    }
    
    # Extract transaction ID (TxId)
    txid_match = re.search(r'TxId:\s*(\d+)', sms_body)
    if txid_match:
        transaction['txid'] = txid_match.group(1)
    
    # Extract amount - look for patterns like "X,XXX RWF" or "X RWF"
    amount_match = re.search(r'([\d,]+)\s*RWF', sms_body)
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '')
        transaction['amount'] = float(amount_str)
    
    # Extract transaction type from context
    if 'transferred' in sms_body.lower():
        transaction['type'] = 'TRANSFER'
        # Extract receiver name
        receiver_match = re.search(r'transferred.*?to\s+([A-Za-z\s]+)\s*\(', sms_body)
        if receiver_match:
            transaction['receiver'] = receiver_match.group(1).strip()
    elif 'payment' in sms_body.lower() or 'paid' in sms_body.lower():
        transaction['type'] = 'PAYMENT'
        # Extract receiver name
        receiver_match = re.search(r'payment of.*?to\s+([A-Za-z\s\d]+)', sms_body)
        if receiver_match:
            transaction['receiver'] = receiver_match.group(1).strip()
    elif 'deposit' in sms_body.lower():
        transaction['type'] = 'DEPOSIT'
        transaction['receiver'] = 'Self'
    elif 'withdrawal' in sms_body.lower() or 'withdrawn' in sms_body.lower():
        transaction['type'] = 'WITHDRAWAL'
        transaction['receiver'] = 'Withdrawal'
    elif 'received' in sms_body.lower():
        transaction['type'] = 'RECEIVED'
        # Extract sender name
        sender_match = re.search(r'received\s+[\d,]+\s+RWF\s+from\s+([A-Za-z\s]+)\s*\(', sms_body)
        if sender_match:
            transaction['sender'] = sender_match.group(1).strip()
    else:
        transaction['type'] = 'OTHER'
    
    # Extract fee if present
    fee_match = re.search(r'Fee\s+(?:was)?:?\s*([\d,]+)\s*RWF', sms_body)
    if fee_match:
        fee_str = fee_match.group(1).replace(',', '')
        transaction['fee'] = float(fee_str)
    
    # Extract new balance if present
    balance_match = re.search(r'[Nn]ew\s+balance:?\s*([\d,]+)\s*RWF', sms_body)
    if balance_match:
        balance_str = balance_match.group(1).replace(',', '')
        transaction['new_balance'] = float(balance_str)
    
    return transaction


def parse_xml_to_json(xml_file_path):
    """
    Parse XML file containing SMS transactions and convert to JSON format
    
    Args:
        xml_file_path (str): Path to the XML file
        
    Returns:
        list: List of transaction dictionaries
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        transactions = []
        transaction_id = 1
        
        # Iterate through each SMS element
        for idx, sms in enumerate(root.findall('sms'), 1):
            # Extract SMS attributes
            sms_data = {
                'address': sms.get('address'),
                'date': sms.get('date'),
                'readable_date': sms.get('readable_date'),
                'type': sms.get('type'),
                'body': sms.get('body'),
                'status': sms.get('status'),
                'read': sms.get('read'),
                'service_center': sms.get('service_center'),
                'date_sent': sms.get('date_sent'),
                'contact_name': sms.get('contact_name')
            }
            
            # Extract transaction from SMS body
            transaction = extract_transaction_from_sms(sms_data.get('body'), sms_data)
            
            if transaction:
                # Add unique ID
                transaction['id'] = transaction_id
                transaction_id += 1
                transactions.append(transaction)
        
        return transactions
    
    except FileNotFoundError:
        print(f"Error: XML file not found at {xml_file_path}")
        return []
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error parsing XML: {e}")
        return []


def save_to_json_file(data, output_file='transactions.json'):
    """
    Save parsed data to a JSON file
    
    Args:
        data (list): List of transaction dictionaries
        output_file (str): Output JSON file path
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")


if __name__ == "__main__":
    # Parse XML file
    xml_path = '../modified_sms_v2.xml'
    transactions = parse_xml_to_json(xml_path)
    
    # Display parsed data
    print(f"Successfully parsed {len(transactions)} transactions")
    print("\nFirst 3 transactions:")
    for trans in transactions[:3]:
        print(json.dumps(trans, indent=2))
    
    # Save to JSON file
    save_to_json_file(transactions, 'transactions.json')
