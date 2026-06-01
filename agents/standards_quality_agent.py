from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class StandardsQualityAgent:
    def __init__(self):
        self.name = "Standards & Quality"
        self.agent_key = "standards_quality"
        
    def get_system_prompt(self) -> str:
        """
        Strict JSON-only system prompt for Standards & Quality compliance analysis
        """
        return """CRITICAL: You MUST respond with ONLY valid JSON. No explanations, no markdown, no extra text. Start with { and end with }. Invalid JSON will cause system failure.

You are a Standards & Quality compliance agent. Analyze content for quality and accuracy issues.

SCORING (0.0-1.0, where 1.0 = high quality):
- ≥0.8: "none" (good quality)
- 0.6-0.7: "low-risk" (minor issues)
- 0.3-0.5: "medium-risk" (quality concerns)
- <0.3: "high-risk" (poor quality)

VIOLATION TYPES (max 3, only if significant):
["quality_issue", "accuracy_concern", "completeness_gap"]

REQUIREMENTS:
- Keep reasoning to 1 concise sentence
- Keep findings to 1 sentence each (max 2)
- Keep recommendations to 1 sentence each (max 2)
- Only flag ACTUAL quality problems, not normal content
- Simple greetings/conversations should score 0.8+ with no violations

RETURN ONLY THIS JSON FORMAT:
{
    "score": 0.0-1.0,
    "flag_type": "none/low-risk/medium-risk/high-risk",
    "violations": ["violation1", "violation2"],
    "reasoning": "One sentence explaining the score",
    "specific_findings": ["One finding sentence"],
    "recommendations": ["One recommendation sentence"]
}"""

    def create_analysis_prompt(self, llm_output: str) -> str:
        """
        Create the complete prompt for this agent's analysis
        """
        return f"""{self.get_system_prompt()}

CONTENT TO ANALYZE:
{llm_output}

Analyze the above content thoroughly for quality issues, accuracy problems, and standards compliance. Return only the JSON response as specified."""

    def parse_agent_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the agent's JSON response and add agent metadata
        """
        import json
        
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            
            # Add agent metadata
            result["agent_name"] = self.name
            
            # Validate required fields
            required_fields = ["score", "flag_type", "violations", "reasoning", "specific_findings", "recommendations"]
            for field in required_fields:
                if field not in result:
                    result[field] = [] if field in ["violations", "specific_findings", "recommendations"] else ""
            
            # Ensure score is float between 0 and 1
            result["score"] = max(0.0, min(1.0, float(result.get("score", 0.5))))
            
            # Validate flag_type
            valid_flags = ["none", "low-risk", "medium-risk", "high-risk"]
            if result.get("flag_type") not in valid_flags:
                # Auto-determine flag based on score
                score = result["score"]
                if score >= 0.8:
                    result["flag_type"] = "none"
                elif score >= 0.6:
                    result["flag_type"] = "low-risk"
                elif score >= 0.3:
                    result["flag_type"] = "medium-risk"
                else:
                    result["flag_type"] = "high-risk"
            
            logger.info(f"Standards Quality Agent analysis complete. Score: {result['score']}, Flag: {result['flag_type']}")
            
            return result
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse Standards Quality Agent response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            
            # Return fallback response
            return {
                "agent_name": self.name,
                "score": 0.5,
                "flag_type": "medium-risk",
                "violations": ["parsing_error"],
                "reasoning": f"Failed to parse agent response: {str(e)}",
                "specific_findings": ["Agent response parsing failed"],
                "recommendations": ["Review agent response format", "Check JSON structure"]
            }
