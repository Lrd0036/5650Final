import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "lrd0036")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
MAKE_TRADE_API_KEY = os.getenv("MAKE_TRADE_API_KEY")
MAKE_TRADE_URL = "https://mothership-crg7hzedd6ckfegv.eastus-01.azurewebsites.net/make_trade"
