// amplify/backend.ts
import { defineBackend } from "@aws-amplify/backend";
import { Stack } from "aws-cdk-lib";
import {
  RestApi,
  LambdaIntegration,
  Deployment,
  Stage,
} from "aws-cdk-lib/aws-apigateway";
import { tradingApiFunction } from "./functions/tradingApi/resource"; // <--- Import your Python function
import { auth } from "./auth/resource";
import { data } from "./data/resource";

const backend = defineBackend({
  auth,
  data,
  tradingApiFunction, // <--- Add the function to the backend definition
});

// --- Custom REST API Stack ---
const customStack = backend.createStack("CustomRestApiStack");

// 1. **CORRECTED LINE**: Access the actual Lambda function instance
const lambdaFunction = backend.tradingApiFunction.resources.lambda; // <--- FIX IS HERE

// 2. Define the Lambda Integration (connects API Gateway to the Lambda)
const integration = new LambdaIntegration(lambdaFunction, {
    // Add request parameters here if needed for API Gateway to map to Lambda
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


// 3. Define the API Gateway
const restApi = new RestApi(customStack, "TradingRestApi", {
  restApiName: "TradingBotApi", // The name that will appear in the AWS console
  description: "REST API for trading bot endpoints and dashboard",
  deployOptions: {
    stageName: "prod", // Use a stage name
  },
});

// 4. Create a Catch-All Proxy Resource
const proxyResource = restApi.root.addResource("{proxy+}");

// 5. Attach the Lambda Integration to the proxy resource for ALL HTTP methods
proxyResource.addMethod("ANY", integration);

// 6. Define the deployment and stage
new Deployment(customStack, "ApiDeployment", {
  api: restApi,
});

new Stage(customStack, "ApiStage", {
    deployment: new Deployment(customStack, 'DeploymentStage', {
        api: restApi
    }),
    stageName: 'prod'
});