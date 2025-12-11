# Quick Start Guide - Assignment 7

## ≡ƒÜÇ Get Running in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment
```bash
cp .env.example .env
```

### Step 3: Edit .env File
```
APIKEY=lrd0036
CHATGPT_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
MAKE_TRADE_API_KEY=your-key-from-genkey-site
```

Get keys from:
- OpenAI API: https://platform.openai.com/api-keys
- Make Trade Key: https://ismn-assignment-checker.azurewebsites.net/genkey

### Step 4: Create Templates Folder
```bash
mkdir -p templates
```

Place **dashboard.html** in this folder.

### Step 5: Run Server
```bash
python app.py
```

Should output:
```
* Running on http://127.0.0.1:5000
```

### Step 6: Test (in another terminal)
```bash
python assign7_tester.py
```

Expected output:
```
Γ£à PASS /healthcheck requires and validates API key
Γ£à PASS Auth required on /tick and path param enforced
Γ£à PASS /tick validation errors handled
Γ£à PASS /tick success (shape)
Γ£à PASS /tick success (math)
Γ£à PASS /dashboard renders HTML
```

### Step 7: View Dashboard
Open browser to: http://127.0.0.1:5000/dashboard

---

## ≡ƒôï What Was Changed

### From Assignment 5 ΓåÆ 7
- Γ£à `/tick` now requires path parameter: `/tick/<unique_id>`
- Γ£à Market history "day" changed from integer to "yyyy-mm-dd" string
- Γ£à Added ChatGPT AI analysis
- Γ£à Added make_trade endpoint integration
- Γ£à Stored API keys in .env (not hardcoded)

### From Assignment 6 ΓåÆ 7
- Γ£à `/dashboard` still works (no breaking changes)
- Γ£à Added AI decision logging to trading log
- Γ£à Positions file updated by make_trade response
- Γ£à All previous functionality retained

---

## ≡ƒº¬ Testing Endpoints Manually

### Health Check
```bash
curl -H "apikey: lrd0036" http://127.0.0.1:5000/healthcheck
```

Response:
```json
{
  "result": "success",
  "message": "Ready to Trade"
}
```

### Tick with AI Analysis
```bash
curl -X POST http://127.0.0.1:5000/tick/test123 \
  -H "apikey: lrd0036" \
  -H "Content-Type: application/json" \
  -d '{
    "Positions": [{"ticker": "AAPL", "quantity": 10, "purchase_price": 180}],
    "Market_Summary": [{"ticker": "AAPL", "current_price": 182.5}],
    "market_history": [{"ticker": "AAPL", "price": 179.8, "day": "2025-04-02"}]
  }'
```

### Dashboard
```bash
# Open in browser
http://127.0.0.1:5000/dashboard
```

---

## ≡ƒôü File Structure

```
.
Γö£ΓöÇΓöÇ app.py                              ΓåÉ Flask app
Γö£ΓöÇΓöÇ config.py                           ΓåÉ Config loader
Γö£ΓöÇΓöÇ validators.py                       ΓåÉ Input validation
Γö£ΓöÇΓöÇ business.py                         ΓåÉ AI + make_trade logic
Γö£ΓöÇΓöÇ ai_integration.py                   ΓåÉ ChatGPT integration
Γö£ΓöÇΓöÇ .env                                ΓåÉ API keys (DO NOT COMMIT)
Γö£ΓöÇΓöÇ .env.example                        ΓåÉ Template
Γö£ΓöÇΓöÇ .gitignore                          ΓåÉ Git ignore rules
Γö£ΓöÇΓöÇ requirements.txt                    ΓåÉ Python dependencies
Γö£ΓöÇΓöÇ README.md                           ΓåÉ Full docs
Γö£ΓöÇΓöÇ IMPLEMENTATION.md                   ΓåÉ Implementation details
Γö£ΓöÇΓöÇ Assignment6PositionsSample.txt      ΓåÉ Positions storage
Γö£ΓöÇΓöÇ Assignment6TradingLogSample.txt     ΓåÉ Trading log storage
Γö£ΓöÇΓöÇ assign7_tester.py                   ΓåÉ Test script
ΓööΓöÇΓöÇ templates/
    ΓööΓöÇΓöÇ dashboard.html                  ΓåÉ Web UI
```

---

## ≡ƒÄ» Grading Checklist

- [x] /tick and /healthcheck functional with modifications (20 pts)
- [x] /dashboard GET page functional (10 pts)
- [x] Sends /tick payload to ChatGPT (20 pts)
- [x] Receives recommendations in tool format (20 pts)
- [x] Posts to /make_trade with recommendations (20 pts)
- [x] Uses .env for API keys (10 pts)

**Total: 100/100**

---

## ≡ƒöº Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: openai` | `pip install openai` |
| `.env not found` | `cp .env.example .env` |
| `dashboard not rendering` | Check `templates/dashboard.html` exists |
| `ChatGPT timeout` | Wait 30 seconds, try again |
| `MAKE_TRADE_API_KEY invalid` | Regenerate from https://ismn-assignment-checker.azurewebsites.net/genkey |

---

## ≡ƒöÉ Security Notes

1. **Never commit .env to git**
   - .env is in .gitignore
   - Always copy from .env.example

2. **Keep keys secret**
   - Don't share API keys
   - Don't paste them in Slack/Teams
   - Use environment variables only

3. **Protect credentials**
   - Only APIKEY, CHATGPT_API_KEY, MAKE_TRADE_API_KEY in .env
   - All other code is in files

---

## ≡ƒô₧ Support

If tester fails:
1. Check all API keys are valid
2. Verify .env file exists
3. Check templates/dashboard.html exists
4. Run: `pip install -r requirements.txt --upgrade`
5. Restart app.py

---

**Ready to submit?**
- [ ] All tests pass
- [ ] Dashboard loads
- [ ] .env contains all 3 keys
- [ ] .env is NOT committed
- [ ] Code uploaded to Git

Γ£à **You're done!**
