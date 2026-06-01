"""
AWS Lambda handler for AI Governance Middleware
"""
import json
import os
from mangum import Mangum
from main import app

# Create the Lambda handler using Mangum
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    AWS Lambda entry point
    """
    try:
        # Log the event for debugging
        print(f"Lambda event: {json.dumps(event, default=str)}")
        
        # Use Mangum to handle the FastAPI app
        response = handler(event, context)
        
        # Log the response for debugging
        print(f"Lambda response: {json.dumps(response, default=str)}")
        
        return response
        
    except Exception as e:
        print(f"Lambda handler error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        }
