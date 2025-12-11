# Quick Start Guide for Assignment 4

## Step-by-Step Setup (5 minutes)

### Step 1: Get Your API Key (1 min)
1. Open: https://ismn-assignment-checker.azurewebsites.net/genkey
2. Copy the generated API key

### Step 2: Install Dependencies (1 min)
```bash
pip install pandas python-dotenv requests
```

### Step 3: Create .env File (1 min)
1. Copy `.env.example` to `.env`
2. Edit `.env` and paste your API key:

```
api-key=paste_your_key_here
input-filepath=Inventory.csv
error-filepath=errors.csv
```

### Step 4: Test the Logic (Optional - 1 min)
```bash
python test_validation.py
```

This shows you what will be sent without actually calling the API.

### Step 5: Run the Assignment (1 min)
```bash
python main.py
```

Expected output:
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

### Step 6: Submit to Git
```bash
git init
git add main.py requirements.txt .gitignore README.md Inventory.csv
git commit -m "Assignment 4 submission"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

**IMPORTANT:** DO NOT commit the .env file!

## Files You Created
- ✓ main.py - Main script (submit this)
- ✓ requirements.txt - Dependencies (submit this)
- ✓ .gitignore - Git ignore rules (submit this)
- ✓ .env - Your API key (DO NOT SUBMIT)
- ✓ errors.csv - Generated when you run (DO NOT SUBMIT)

## Grading Checklist
- [ ] API key in .env file (not hardcoded)
- [ ] Input filepath in .env file
- [ ] Error filepath in .env file
- [ ] Console output matches specification
- [ ] JSON payload has correct format
- [ ] Summary calculations match detail records
- [ ] Error file has NO header row
- [ ] All 5 error rows detected
- [ ] Code uploaded to Git
- [ ] .env NOT committed to Git

## Expected Results
- **Valid records:** 25
- **Error records:** 5
- **Amount sum:** 3950
- **Quantity sum:** 245

## Troubleshooting
| Issue | Solution |
|-------|----------|
| "api-key not found" | Create .env file from .env.example |
| "File not found" | Ensure Inventory.csv is in same folder |
| API error | Check your API key is valid |
| Wrong calculations | Run test_validation.py to debug |

## Need Help?
1. Run `python test_validation.py` to see what your code will do
2. Check the README.md for detailed documentation
3. Verify your .env file is configured correctly
