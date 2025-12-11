
# Create the main Python script for the assignment

main_py_content = '''import os
import pandas as pd
import requests
import json
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Get environment variables
    api_key = os.getenv('api-key')
    input_filepath = os.getenv('input-filepath')
    error_filepath = os.getenv('error-filepath')
    
    # Validate environment variables exist
    if not api_key:
        print("ERROR: api-key not found in environment variables")
        return
    if not input_filepath:
        print("ERROR: input-filepath not found in environment variables")
        return
    if not error_filepath:
        print("ERROR: error-filepath not found in environment variables")
        return
    
    # Extract filename for console output
    filename = os.path.basename(input_filepath)
    print(f"Processing {filename}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_filepath)
        
        # Initialize lists for valid and error rows
        valid_rows = []
        error_rows = []
        
        # Process each row
        for index, row in df.iterrows():
            # Check for missing required fields (ID, AMOUNT, ITEM, QUANTITY)
            # Note: STATE is NOT required per assignment specs
            missing_fields = []
            
            if pd.isna(row['ID']):
                missing_fields.append('ID')
            if pd.isna(row['Amount']):
                missing_fields.append('AMOUNT')
            if pd.isna(row['Item']):
                missing_fields.append('ITEM')
            if pd.isna(row['Quantity']):
                missing_fields.append('QUANTITY')
            
            if missing_fields:
                # Row has errors - add to error list
                error_code = ', '.join(missing_fields)
                error_row = {
                    'ID': row['ID'] if not pd.isna(row['ID']) else '',
                    'AMOUNT': row['Amount'] if not pd.isna(row['Amount']) else '',
                    'ITEM': row['Item'] if not pd.isna(row['Item']) else '',
                    'QUANTITY': row['Quantity'] if not pd.isna(row['Quantity']) else '',
                    'STATE': row['State'] if not pd.isna(row['State']) else '',
                    'ERRORCODE': error_code
                }
                error_rows.append(error_row)
            else:
                # Row is valid - add to valid list
                valid_row = {
                    'ID': int(row['ID']),
                    'AMOUNT': int(row['Amount']),
                    'ITEM': row['Item'],
                    'QUANTITY': int(row['Quantity']),
                    'STATE': row['State'] if not pd.isna(row['State']) else None
                }
                valid_rows.append(valid_row)
        
        # Calculate summary values
        detail_count = len(valid_rows)
        amount_sum = sum(row['AMOUNT'] for row in valid_rows)
        quantity_sum = sum(row['QUANTITY'] for row in valid_rows)
        
        # Build JSON payload
        payload = {
            'summary': {
                'detail_count': detail_count,
                'amount_sum': amount_sum,
                'quantity_sum': quantity_sum
            },
            'details': valid_rows
        }
        
        # POST to API
        api_url = 'https://reportingassignment-a0evaccsgzg9efhv.eastus-01.azurewebsites.net/api/Reporting'
        headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("Data successfully submitted to the API.")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
        
        # Handle errors
        if error_rows:
            # Write error file WITHOUT header row
            error_df = pd.DataFrame(error_rows)
            error_df.to_csv(error_filepath, index=False, header=False)
            
            # Display errors to console
            print("Errors:")
            print("ID AMOUNT ITEM QUANTITY STATE ERRORCODE")
            for error in error_rows:
                print(f"{error['ID']} {error['AMOUNT']} {error['ITEM']} {error['QUANTITY']} {error['STATE']} {error['ERRORCODE']}")
        else:
            print("No Inventory error rows detected.")
        
        print("Processing Complete.")
        
    except FileNotFoundError:
        print(f"ERROR: File not found: {input_filepath}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()
'''

# Save the main.py file
with open('main.py', 'w') as f:
    f.write(main_py_content)

print("✓ main.py created")
