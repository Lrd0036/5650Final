# amplify/functions/tradingApi/lambda_handler.py
# import awsgi  <-- REMOVE THIS
import wsgi_sls as awsgi # Use the new package with an alias for minimal code change
from app import app

# This function is the entry point that AWS Lambda will call
def handler(event, context):
    # wsgi_sls.response is the equivalent function for the new package
    return awsgi.response(app, event, context)