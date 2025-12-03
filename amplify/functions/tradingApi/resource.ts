import { defineFunction } from '@aws-amplify/backend';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import * as path from 'path';

// Get the directory containing this file
const functionDir = path.dirname(new URL(import.meta.url).pathname);

export const tradingApiFunction = defineFunction({
    name: 'TradingApiFunction',
    // Point the entry to the Python code folder
    entry: path.join(functionDir),
    // Use the latest Python runtime
    runtime: Runtime.PYTHON_3_12, 
    // Lambda entry point: lambda_handler.py :: handler function
    handler: 'lambda_handler.handler', 
    // Increase timeout for the ChatGPT call (20 seconds recommended)
    timeout: 20, 
});