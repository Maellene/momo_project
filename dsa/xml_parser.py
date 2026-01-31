"""
XML Parser Module
Parses modified_sms_v2.xml and converts SMS records to JSON format
Author: Person 1
"""

import xml.etree.ElementTree as ET
import json


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
        
        # Iterate through each transaction element
        for transaction in root.findall('transaction'):
            # Extract transaction data
            trans_dict = {
                'id': int(transaction.get('id')),
                'type': transaction.find('type').text,
                'amount': float(transaction.find('amount').text),
                'sender': transaction.find('sender').text,
                'receiver': transaction.find('receiver').text,
                'timestamp': transaction.find('timestamp').text,
                'status': transaction.find('status').text,
                'fee': float(transaction.find('fee').text)
            }
            
            transactions.append(trans_dict)
        
        return transactions
    
    except Exception as e:
        print(f"Error parsing XML: {e}")
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
