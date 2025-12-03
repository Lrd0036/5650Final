// amplify/backend.ts

// ----------------------------------------------------
// IMPORTS
// ----------------------------------------------------
import { defineBackend } from "@aws-amplify/backend";
import { Stack, Duration } from "aws-cdk-lib";
import {
  RestApi,
  LambdaIntegration,
  Deployment,
  Stage,
} from "aws-cdk-lib/aws-apigateway";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as path from "path"; // This should now work after npm install
import { auth } from "./auth/resource";
import { data } from "./data/resource";

// ----------------------------------------------------
// BACKEND DEFINITION
// ----------------------------------------------------
const backend = defineBackend({
  auth,
  data,
  // Note: The Python function is NOT listed here because it is a custom CDK resource.
});

// ----------------------------------------------------
// CUSTOM REST API AND PYTHON FUNCTION STACK
// ----------------------------------------------------

// 1. Create a custom CDK stack for the API and Python Function
const customStack = backend.createStack("CustomPythonApiStack");

// 2. Define the Python Lambda Function using the full CDK Construct
const pythonFunction = new lambda.Function(customStack, 'TradingApiFunction', {
    // Must specify Python runtime and point to the handler file you created
    runtime: lambda.Runtime.PYTHON_3_12,
    handler: 'lambda_handler.handler', // lambda_handler.py :: handler function
    // 💡 FIX for __dirname/path issues: Use path.resolve from the current process's directory
    code: lambda.Code.fromAsset(path.resolve('amplify', 'functions', 'tradingApi')), 
    timeout: Duration.seconds(30), // Increased timeout for external calls (ChatGPT)
});

// 3. Define the Lambda Integration (connects API Gateway to the Lambda)
const integration = new LambdaIntegration(pythonFunction, {
    // Standard VTL template for Flask/Proxy Integration
    requestTemplates: {
        "application/json": `{
            "body": $input.json('$'),
            "headers": {
                #foreach($header in $input.params().header.keySet())
                "$header": "$util.escapeJavaScript($input.params().header.get($header))"
                #end
            },
            "path": "$input.params().path",
            "queryStringParameters": {
                #foreach($param in $input.params().querystring.keySet())
                "$param": "$util.escapeJavaScript($input.params().querystring.get($param))"
                #end
            }
        }`
    }
});

// 4. Define the API Gateway
const restApi = new RestApi(customStack, "TradingRestApi", {
  restApiName: "TradingBotApi", 
  description: "REST API for trading bot endpoints and dashboard",
  deployOptions: {
    stageName: "prod",
  },
});

// 5. Create a Catch-All Proxy Resource (routes all traffic to the Lambda)
const proxyResource = restApi.root.addResource("{proxy+}");
proxyResource.addMethod("ANY", integration);

// 6. Define the deployment and stage
// Create a single Deployment resource with a new unique ID (e.g., v3)
const apiDeployment = new Deployment(customStack, 'TradingApiDeploymentV3', { // <-- CHANGED ID HERE
    api: restApi,
});

// Create the Stage resource and link it directly to the single Deployment.
new Stage(customStack, "ProdStageV3", { // <-- CHANGED ID HERE
    deployment: apiDeployment,
    stageName: "prod",
});