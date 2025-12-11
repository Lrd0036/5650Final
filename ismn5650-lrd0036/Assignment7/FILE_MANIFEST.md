# File Manifest - Assignment 7

## ≡ƒôª Complete File List

### Core Application Files (MODIFY EXISTING)

#### 1. **app.py** Γ¡É MODIFIED
- **Purpose**: Main Flask application
- **Changes**: 
  - Added `/tick/<tick_id>` path parameter support
  - Passes tick_id to analyze_tick_payload()
- **Key Routes**:
  - `GET /healthcheck` - Health check (authenticated)
  - `POST /tick/<tick_id>` - Tick processing with AI (authenticated)
  - `GET /dashboard` - Web dashboard (public)

#### 2. **config.py** Γ¡É MODIFIED
- **Purpose**: Configuration management
- **Changes**: 
  - Now loads from .env using python-dotenv
  - Stores CHATGPT_API_KEY and MAKE_TRADE_API_KEY
- **Key Variables**:
  - `APIKEY` - Student API key
  - `CHATGPT_API_KEY` - OpenAI API key
  - `MAKE_TRADE_API_KEY` - Make trade endpoint key
  - `MAKE_TRADE_URL` - Mothership endpoint

#### 3. **business.py** Γ¡É MODIFIED  
- **Purpose**: Business logic and AI integration
- **Changes**:
  - `analyze_tick_payload(payload, tick_id)` now accepts tick_id
  - Calls `get_chatgpt_analysis()` for AI recommendations
  - Posts to make_trade via `post_to_make_trade()`
  - Updates positions from make_trade response
- **Key Functions**:
  - `analyze_tick_payload()` - Main processing
  - `post_to_make_trade()` - Makes trade API call
  - `get_positions()` - Read positions file
  - `get_trading_log()` - Read trading log
  - `save_positions()` - Write positions file
  - `append_to_trading_log()` - Append to log

#### 4. **validators.py** Γ£à UNCHANGED
- **Purpose**: Input validation
- **Keep As-Is**: No changes needed
- **Note**: Already handles both "Positions" and "positions" keys

### New AI Integration Files (CREATE NEW)

#### 5. **ai_integration.py** Γ¡É NEW
- **Purpose**: ChatGPT integration module
- **Key Functions**:
  - `get_chatgpt_analysis(payload)` - Main AI function
    - Sends positions and market data to ChatGPT
    - Returns list of BUY/SELL/STAY recommendations
    - Uses gpt-4 model
  - `parse_openai_tool_call()` - Alternative parsing (optional)
- **Dependencies**: openai library

### Configuration & Environment Files (CREATE NEW)

#### 6. **.env.example** Γ¡É NEW
- **Purpose**: Template for environment variables
- **Content**:
  ```
  APIKEY=lrd0036
  CHATGPT_API_KEY=your_openai_api_key_here
  MAKE_TRADE_API_KEY=your_make_trade_api_key_from_genkey_site
  ```
- **Usage**: Copy to `.env` and fill in actual keys
- **Important**: Add .env to .gitignore

#### 7. **.env** Γ¡É NEW (USER CREATES)
- **Purpose**: Runtime configuration
- **Action**: Create by copying .env.example
- **Content**: Your actual API keys
- **Security**: NEVER commit this file

#### 8. **.gitignore** Γ¡É NEW
- **Purpose**: Prevent committing sensitive files
- **Includes**:
  - `.env` and `.env.local`
  - `__pycache__/` and `*.pyc`
  - `.vscode/` and `.idea/`
  - `venv/` and `ENV/`

#### 9. **requirements.txt** Γ¡É MODIFIED
- **Purpose**: Python dependencies
- **Updated Content**:
  ```
  flask==3.1.2
  python-dotenv==1.0.1
  requests==2.31.0
  openai==1.12.0
  ```
- **New Packages**:
  - `openai==1.12.0` - ChatGPT API
  - `requests==2.31.0` - HTTP requests for make_trade

### Web UI Files (CREATE NEW)

#### 10. **templates/dashboard.html** Γ¡É NEW
- **Purpose**: Web dashboard UI
- **Location**: Must be in `templates/` folder
- **Features**:
  - Display current positions
  - Show P&L calculations
  - Display trading log (reverse chronological)
  - Color-coded actions (BUY=green, SELL=red, STAY=gray, TICK=blue)
  - Responsive design
  - No authentication required

### Documentation Files (CREATE NEW)

#### 11. **README.md** Γ¡É NEW
- **Purpose**: Comprehensive project documentation
- **Includes**:
  - Feature list
  - Project structure
  - Setup instructions
  - API endpoint documentation
  - Testing guide
  - Troubleshooting section

#### 12. **IMPLEMENTATION.md** Γ¡É NEW
- **Purpose**: Implementation details
- **Includes**:
  - Files created/modified list
  - Key changes from Assignment 5 & 6
  - Setup instructions with examples
  - API flow diagram
  - Testing checklist
  - Rubric coverage matrix
  - Troubleshooting guide

#### 13. **QUICKSTART.md** Γ¡É NEW
- **Purpose**: Quick start guide
- **Includes**:
  - 5-minute setup
  - What was changed
  - Manual testing commands
  - File structure
  - Common issues & fixes
  - Security notes

#### 14. **FILE_MANIFEST.md** (this file) Γ¡É NEW
- **Purpose**: Complete file reference
- **Lists**: All files with purpose and location

### Data Files (RETAIN EXISTING)

#### 15. **Assignment6PositionsSample.txt** Γ£à EXISTING
- **Purpose**: Persistent positions storage
- **Format**: JSON array of positions
- **Updated By**: `save_positions()` function
- **Read By**: `get_positions()` function

#### 16. **Assignment6TradingLogSample.txt** Γ£à EXISTING
- **Purpose**: Persistent trading history
- **Format**: JSON array of log entries
- **Updated By**: `append_to_trading_log()` function
- **Read By**: `get_trading_log()` function

### Test Files (EXISTING)

#### 17. **assign7_tester.py** Γ£à EXISTING
- **Purpose**: Assignment 7 test script
- **Tests**:
  - `/healthcheck` authentication
  - `/tick/<id>` path parameter enforcement
  - `/tick` validation errors
  - `/tick` success with math verification
  - `/dashboard` HTML rendering
- **Usage**: `python assign7_tester.py`
- **Note**: Update API_KEY to your student ID

#### 18. **assign5_tester.py** Γ£à EXISTING
- **Purpose**: Assignment 5 backward compatibility
- **Status**: Should still pass (Assignment 7 is backward compatible)

---

## ≡ƒùé∩╕Å Directory Structure

```
project_root/
Γöé
Γö£ΓöÇΓöÇ app.py                                  ΓåÉ Main Flask app
Γö£ΓöÇΓöÇ config.py                               ΓåÉ Configuration
Γö£ΓöÇΓöÇ business.py                             ΓåÉ Business logic
Γö£ΓöÇΓöÇ validators.py                           ΓåÉ Input validation
Γö£ΓöÇΓöÇ ai_integration.py                       ΓåÉ ChatGPT integration
Γöé
Γö£ΓöÇΓöÇ .env                                    ΓåÉ API keys (CREATE, DON'T COMMIT)
Γö£ΓöÇΓöÇ .env.example                            ΓåÉ Template (COMMIT)
Γö£ΓöÇΓöÇ .gitignore                              ΓåÉ Git rules (COMMIT)
Γöé
Γö£ΓöÇΓöÇ requirements.txt                        ΓåÉ Dependencies (COMMIT)
Γö£ΓöÇΓöÇ README.md                               ΓåÉ Main docs (COMMIT)
Γö£ΓöÇΓöÇ IMPLEMENTATION.md                       ΓåÉ Implementation details (COMMIT)
Γö£ΓöÇΓöÇ QUICKSTART.md                           ΓåÉ Quick start (COMMIT)
Γö£ΓöÇΓöÇ FILE_MANIFEST.md                        ΓåÉ This file (COMMIT)
Γöé
Γö£ΓöÇΓöÇ Assignment6PositionsSample.txt          ΓåÉ Positions storage
Γö£ΓöÇΓöÇ Assignment6TradingLogSample.txt         ΓåÉ Trading log storage
Γöé
Γö£ΓöÇΓöÇ assign7_tester.py                       ΓåÉ Test script
Γö£ΓöÇΓöÇ assign5_tester.py                       ΓåÉ Legacy test
Γöé
ΓööΓöÇΓöÇ templates/
    ΓööΓöÇΓöÇ dashboard.html                      ΓåÉ Web UI (CREATE)
```

---

## ≡ƒô¥ File Modification Checklist

### Step 1: MODIFY Existing Files
- [ ] Update `app.py` with new `/tick/<tick_id>` route
- [ ] Update `config.py` with .env loading
- [ ] Update `business.py` with AI integration
- [ ] Update `requirements.txt` with new packages

### Step 2: CREATE New Python Files
- [ ] Create `ai_integration.py` with ChatGPT functions

### Step 3: CREATE Configuration Files
- [ ] Create `.env.example` template
- [ ] Create `.gitignore` rules
- [ ] Create `.env` file (copy from .env.example)

### Step 4: CREATE UI Files
- [ ] Create `templates/` folder
- [ ] Create `templates/dashboard.html` inside folder

### Step 5: CREATE Documentation
- [ ] Create `README.md`
- [ ] Create `IMPLEMENTATION.md`
- [ ] Create `QUICKSTART.md`
- [ ] Create `FILE_MANIFEST.md`

### Step 6: VERIFY & TEST
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python app.py`
- [ ] Run `python assign7_tester.py`
- [ ] Open http://127.0.0.1:5000/dashboard
- [ ] Verify all tests pass

### Step 7: GIT COMMIT
- [ ] Do NOT commit `.env` (should be in .gitignore)
- [ ] Commit all other files
- [ ] Push to GitHub

---

## ≡ƒöä Assignment 5 ΓåÆ 6 ΓåÆ 7 Compatibility

| Feature | Assign 5 | Assign 6 | Assign 7 |
|---------|----------|----------|----------|
| `/healthcheck` | Γ£à | Γ£à | Γ£à |
| `/tick` route | Γ£à | Γ£à | Γ£à Modified |
| Path parameter | Γ¥î | Γ¥î | Γ£à NEW |
| Day format | Integer | Integer | String (yyyy-mm-dd) |
| `/dashboard` | Γ¥î | Γ£à | Γ£à |
| AI Analysis | Γ¥î | Γ¥î | Γ£à NEW |
| make_trade call | Γ¥î | Γ¥î | Γ£à NEW |
| .env support | Γ¥î | Γ¥î | Γ£à NEW |

---

## ≡ƒôª Installation Order

1. Modify existing files (app.py, config.py, business.py, requirements.txt)
2. Create ai_integration.py
3. Create .env.example
4. Create .gitignore
5. Create templates/dashboard.html
6. Create documentation files
7. Run `pip install -r requirements.txt`
8. Create .env file (copy from .env.example)
9. Fill in API keys in .env
10. Run tests

---

## Γ£à Success Criteria

- [x] All tests pass
- [x] `/tick/<id>` accepts path parameter
- [x] ChatGPT analysis works
- [x] make_trade posting works
- [x] Dashboard renders
- [x] .env stores all keys
- [x] No keys in source code
- [x] .env not committed

**You're ready to submit!** ≡ƒÄë
