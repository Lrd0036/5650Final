import pandas as pd
import json

def test_validation():
    """Test the validation logic with the Inventory.csv file"""

    # Read the CSV file
    df = pd.read_csv('Inventory.csv')

    print("="*60)
    print("TESTING VALIDATION LOGIC")
    print("="*60)

    valid_rows = []
    error_rows = []

    # Process each row
    for index, row in df.iterrows():
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
            print(f"Row {index}: ERROR - Missing {error_code}")
        else:
            valid_row = {
                'ID': int(row['ID']),
                'AMOUNT': int(row['Amount']),
                'ITEM': row['Item'],
                'QUANTITY': int(row['Quantity']),
                'STATE': row['State'] if not pd.isna(row['State']) else None
            }
            valid_rows.append(valid_row)

    # Calculate summary
    detail_count = len(valid_rows)
    amount_sum = sum(row['AMOUNT'] for row in valid_rows)
    quantity_sum = sum(row['QUANTITY'] for row in valid_rows)

    print("\n" + "="*60)
    print("SUMMARY RESULTS")
    print("="*60)
    print(f"Total rows in CSV: {len(df)}")
    print(f"Valid rows: {detail_count}")
    print(f"Error rows: {len(error_rows)}")
    print(f"Amount sum: {amount_sum}")
    print(f"Quantity sum: {quantity_sum}")

    print("\n" + "="*60)
    print("ERROR ROWS")
    print("="*60)
    if error_rows:
        print("ID AMOUNT ITEM QUANTITY STATE ERRORCODE")
        for error in error_rows:
            print(f"{error['ID']} {error['AMOUNT']} {error['ITEM']} {error['QUANTITY']} {error['STATE']} {error['ERRORCODE']}")
    else:
        print("No errors detected!")

    # Build sample JSON payload
    payload = {
        'summary': {
            'detail_count': detail_count,
            'amount_sum': amount_sum,
            'quantity_sum': quantity_sum
        },
        'details': valid_rows
    }

    print("\n" + "="*60)
    print("SAMPLE JSON PAYLOAD (first 3 detail records)")
    print("="*60)
    sample_payload = {
        'summary': payload['summary'],
        'details': payload['details'][:3]
    }
    print(json.dumps(sample_payload, indent=2))

    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)
    print(f"✓ {detail_count} valid records ready for API submission")
    print(f"✓ {len(error_rows)} error records ready for error file")

if __name__ == "__main__":
    test_validation()
