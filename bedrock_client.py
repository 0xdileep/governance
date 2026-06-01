import json
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import os
from typing import Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class BedrockClient:
    def __init__(self):
        # Load all configuration from environment variables
        self.region = os.getenv('AWS_REGION')
        self.model_id = os.getenv('BEDROCK_MODEL_ID')
        
        # Validate required environment variables
        if not self.region:
            raise ValueError("AWS_REGION environment variable is required")
        if not self.model_id:
            raise ValueError("BEDROCK_MODEL_ID environment variable is required")
        
        # Validate AWS credentials are available
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if not self.aws_access_key or not self.aws_secret_key:
            logger.warning("AWS credentials not found in environment variables. Using default credential chain.")
        
        # Initialize AWS session for signing requests
        self.session = boto3.Session()
        self.credentials = self.session.get_credentials()
        
        # Bedrock Runtime endpoint
        self.endpoint_url = f"https://bedrock-runtime.{self.region}.amazonaws.com"
        
        logger.info(f"BedrockClient initialized with model: {self.model_id} in region: {self.region}")
        
    def _sign_request(self, request: AWSRequest) -> None:
        """Sign the AWS request using SigV4"""
        SigV4Auth(self.credentials, 'bedrock', self.region).add_auth(request)
    
    def invoke_model(self, prompt: str, max_tokens: int = 4000) -> Dict[str, Any]:
        """
        Invoke Llama model via Bedrock REST API
        """
        try:
            logger.info(f"Making Bedrock API call to {self.model_id} with prompt length: {len(prompt)}")
            
            # Llama format payload
            payload = {
                "prompt": prompt,
                "max_gen_len": max_tokens,
                "temperature": 0.1,  # Low temperature for consistent compliance analysis
                "top_p": 0.9
            }
            
            logger.info(f"Using Llama payload format for model: {self.model_id}")
            
            # Create the request URL
            url = f"{self.endpoint_url}/model/{self.model_id}/invoke"
            logger.info(f"Calling Bedrock URL: {url}")
            
            # Create AWS request object
            request = AWSRequest(
                method='POST',
                url=url,
                data=json.dumps(payload),
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )
            
            # Sign the request
            self._sign_request(request)
            logger.info("Request signed successfully")
            
            # Make the HTTP request
            response = requests.post(
                url,
                data=request.body,
                headers=dict(request.headers),
                timeout=60  # Add timeout
            )
            
            logger.info(f"Bedrock response status: {response.status_code}")
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            
            logger.info(f"Bedrock API call successful. Response length: {len(str(response_data))}")
            
            return response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise Exception(f"Bedrock API request failed: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise Exception(f"Invalid JSON response from Bedrock: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in Bedrock API call: {str(e)}")
            raise Exception(f"Bedrock API error: {str(e)}")
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """
        Extract the text content from Llama Bedrock response
        """
        try:
            # Llama format: response['generation']
            if 'generation' in response:
                return response['generation']
            
            # Alternative Llama format: response['outputs'][0]['text']
            elif 'outputs' in response and len(response['outputs']) > 0:
                return response['outputs'][0]['text']
            
            # Simple text field fallback
            elif 'text' in response:
                return response['text']
            
            else:
                logger.error(f"Unknown Llama response format. Available keys: {list(response.keys())}")
                logger.error(f"Full response: {json.dumps(response, indent=2)}")
                raise Exception("No content found in Llama Bedrock response")
                
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Failed to extract content from Llama response: {str(e)}")
            logger.error(f"Response structure: {json.dumps(response, indent=2)}")
            raise Exception(f"Invalid Llama response format from Bedrock: {str(e)}")
    
    def batch_analyze(self, llm_output: str, batch_prompt: str) -> str:
        """
        Perform batch analysis using single Bedrock call
        """
        try:
            logger.info("Starting batch analysis with Bedrock")
            
            # Invoke the model
            response = self.invoke_model(batch_prompt, max_tokens=6000)
            
            # Extract content
            content = self.extract_content(response)
            
            logger.info(f"Batch analysis complete. Content length: {len(content)}")
            
            return content
            
        except Exception as e:
            logger.error(f"Batch analysis failed: {str(e)}")
            raise Exception(f"Batch analysis error: {str(e)}")

# Global instance
bedrock_client = BedrockClient()
