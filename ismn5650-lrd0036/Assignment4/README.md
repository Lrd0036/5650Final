# Assignment 4 - ETL Data Transformation

This project reads inventory data from a CSV file, validates required fields, transforms it into JSON format, and submits it to an API endpoint.

## Project Structure

```
assignment-4/
├── main.py                 # Main Python script
├── Inventory.csv          # Input data file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (YOU MUST CREATE THIS)
├── .env.example          # Template for .env file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

## Setup Instructions

### 1. Generate Your API Key

Visit: https://ismn-assignment-checker.azurewebsites.net/genkey

Save your generated API key - you'll need it in step 3.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install pandas python-dotenv requests
```

### 3. Configure Environment Variables

Copy the `.env.example` file to create a `.env` file:

```bash
cp .env.example .env
```

Then edit `.env` and replace `YOUR_API_KEY_HERE` with your actual API key:

```
api-key=your_actual_api_key_here
input-filepath=Inventory.csv
error-filepath=errors.csv
```

**IMPORTANT:** Never commit the `.env` file to Git! It's already listed in `.gitignore`.

## Running the Program

```bash
python main.py
```

## Expected Output

### If successful with errors detected:

```
Processing Inventory.csv
Data successfully submitted to the API.
Errors:
ID AMOUNT ITEM QUANTITY STATE ERRORCODE
4.0 40  30 Louisiana ITEM
 70 Item 7 3 Louisiana ID
17.0 170  10 Florida ITEM
 190 Item 19 10 Florida ID
27.0 270  20 Florida ITEM
Processing Complete.
```

### If successful with no errors:

```
Processing Inventory.csv
Data successfully submitted to the API.
No Inventory error rows detected.
Processing Complete.
```

## How It Works

1. **Extract:** Reads the CSV file specified in `input-filepath`
2. **Transform:** 
   - Validates each row for required fields (ID, AMOUNT, ITEM, QUANTITY)
   - Note: STATE is optional and can be null
   - Separates valid rows from error rows
   - Builds JSON payload with summary and details sections
3. **Load:** 
   - POSTs the JSON payload to the API endpoint
   - Writes error rows to the error file (if any exist)

## Data Validation Rules

Required fields:
- ID (cannot be missing)
- AMOUNT (cannot be missing)
- ITEM (cannot be missing)
- QUANTITY (cannot be missing)

Optional fields:
- STATE (can be null/missing)

Any row missing a required field will be written to the error file with an ERRORCODE indicating which field(s) are missing.

## JSON Payload Format

```json
{
  "summary": {
    "detail_count": 25,
    "amount_sum": 3950,
    "quantity_sum": 245
  },
  "details": [
    {
      "ID": 1,
      "AMOUNT": 10,
      "ITEM": "Item 1",
      "QUANTITY": 30,
      "STATE": "Alabama"
    },
    ...
  ]
}
```

## Error File Format

The error file (`errors.csv`) will contain:
- **NO header row** (as per assignment requirements)
- Columns: ID, AMOUNT, ITEM, QUANTITY, STATE, ERRORCODE
- Only rows that failed validation

## Grading Rubric (100 points)

- ✓ Successfully POSTs data to API: 20 points
- ✓ Proper console messaging: 10 points
- ✓ API Key in environment variable: 5 points
- ✓ Input filepath in environment variable: 5 points
- ✓ Summary JSON meets spec: 10 points
- ✓ Summary values match details: 10 points
- ✓ Details JSON meets spec: 10 points
- ✓ Correct number of detail items: 10 points
- ✓ Error file meets spec: 5 points
- ✓ Error filepath in environment variable: 5 points
- ✓ NO header row in error file: 5 points
- ✓ Correct error rows included: 5 points

## Git Submission

1. Initialize Git repository:

```bash
git init
```

2. Add your files:

```bash
git add main.py requirements.txt .gitignore README.md Inventory.csv
```

**DO NOT add .env file!**

3. Commit:

```bash
git commit -m "Initial commit for Assignment 4"
```

4. Push to your remote repository (GitHub, GitLab, etc.)

## Troubleshooting

### "ERROR: api-key not found in environment variables"
- Make sure you created the `.env` file from `.env.example`
- Verify your API key is correctly entered in `.env`

### "ERROR: File not found"
- Verify `Inventory.csv` is in the same directory as `main.py`
- Check that `input-filepath` in `.env` matches the actual filename

### API returns error status code
- Verify your API key is valid
- Check that your JSON payload format matches the specification
- Ensure summary calculations are correct

## API Documentation

Swagger Documentation: https://app.swaggerhub.com/apis-docs/JFARR3/ismn5650-reportingassignment/1.0.0#/default

API Endpoint: https://reportingassignment-a0evaccsgzg9efhv.eastus-01.azurewebsites.net/api/Reporting

## Support

If you encounter issues:
1. Check the console output for specific error messages
2. Verify all environment variables are set correctly
3. Review the assignment requirements document
4. Test your API key at the generation URL

## License

This is an academic assignment for ISMN 5650.
