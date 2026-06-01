from typing import Dict, Any
import logging
from models import GovernanceResponse

logger = logging.getLogger(__name__)

class ResponseFormatter:
    def __init__(self):
        pass
    
    def format_response(self, original_output: str, agent_results: Dict[str, Any]) -> GovernanceResponse:
        """
        Format the simplified governance response with just agent results
        """
        logger.info("Formatting simplified governance response...")
        
        try:
            # Validate agent results and ensure they have required fields
            validated_results = {}
            for agent_key, result in agent_results.items():
                if isinstance(result, dict):
                    # Ensure all required fields are present
                    validated_result = {
                        "agent_name": result.get("agent_name", agent_key.replace("_", " ").title()),
                        "score": max(0.0, min(1.0, float(result.get("score", 0.5)))),
                        "flag_type": result.get("flag_type", "medium-risk"),
                        "violations": result.get("violations", []),
                        "reasoning": result.get("reasoning", "Analysis completed"),
                        "specific_findings": result.get("specific_findings", []),
                        "recommendations": result.get("recommendations", [])
                    }
                    validated_results[agent_key] = validated_result
                else:
                    # Fallback for invalid result
                    validated_results[agent_key] = {
                        "agent_name": agent_key.replace("_", " ").title(),
                        "score": 0.5,
                        "flag_type": "medium-risk",
                        "violations": ["processing_error"],
                        "reasoning": "Agent response processing failed",
                        "specific_findings": ["Unable to process agent response"],
                        "recommendations": ["Review agent configuration"]
                    }
            
            # Create simplified response - ONLY agent results
            response = GovernanceResponse(
                original_output=original_output,
                governance_results=validated_results
            )
            
            logger.info(f"Simplified response formatted successfully with {len(validated_results)} agents")
            return response
            
        except Exception as e:
            logger.error(f"Failed to format simplified response: {str(e)}")
            
            # Create minimal fallback response
            fallback_results = {}
            for agent_key in ["data_privacy_security", "ai_risk_ethics", "content_platform", "standards_quality", "legal_regulatory"]:
                fallback_results[agent_key] = {
                    "agent_name": agent_key.replace("_", " ").title(),
                    "score": 0.5,
                    "flag_type": "medium-risk",
                    "violations": ["formatting_error"],
                    "reasoning": f"Response formatting failed: {str(e)}",
                    "specific_findings": ["System error prevented analysis"],
                    "recommendations": ["Check system logs and retry"]
                }
            
            return GovernanceResponse(
                original_output=original_output,
                governance_results=fallback_results
            )
