from typing import Dict, Any
import json
import logging
import asyncio
from bedrock_client import bedrock_client
from agents.data_privacy_agent import DataPrivacyAgent
from agents.ai_ethics_agent import AIEthicsAgent
from agents.content_compliance_agent import ContentComplianceAgent
from agents.standards_quality_agent import StandardsQualityAgent
from agents.legal_regulatory_agent import LegalRegulatoryAgent

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self):
        # Initialize all 5 independent agents
        self.agents = {
            "data_privacy_security": DataPrivacyAgent(),
            "ai_risk_ethics": AIEthicsAgent(),
            "content_platform": ContentComplianceAgent(),
            "standards_quality": StandardsQualityAgent(),
            "legal_regulatory": LegalRegulatoryAgent()
        }
        
    
    async def process_agent_individually(self, agent_key: str, agent, llm_output: str) -> Dict[str, Any]:
        """
        Process a single agent with its own dedicated API call
        """
        try:
            logger.info(f"Processing {agent.name} individually")
            
            # Create individual agent prompt
            agent_prompt = agent.create_analysis_prompt(llm_output)
            
            # Individual Bedrock API call for this agent
            response = bedrock_client.invoke_model(agent_prompt, max_tokens=2000)
            content = bedrock_client.extract_content(response)
            
            # Parse agent response
            result = agent.parse_agent_response(content)
            
            logger.info(f"{agent.name} processing complete. Score: {result.get('score', 0.5)}")
            return result
            
        except Exception as e:
            logger.error(f"Individual agent processing failed for {agent.name}: {str(e)}")
            
            # Return error result for this agent
            return {
                "agent_name": agent.name,
                "score": 0.5,
                "flag_type": "medium-risk",
                "violations": ["processing_error"],
                "reasoning": f"Agent processing failed: {str(e)}",
                "specific_findings": ["Individual agent processing error occurred"],
                "recommendations": ["Retry request", "Check agent configuration"]
            }

    async def process_all_agents(self, llm_output: str) -> Dict[str, Any]:
        """
        Process LLM output through all 5 agents concurrently with individual API calls
        """
        try:
            logger.info("Starting concurrent processing of all 5 compliance agents")
            
            # Create concurrent tasks for all agents
            tasks = []
            for agent_key, agent in self.agents.items():
                task = self.process_agent_individually(agent_key, agent, llm_output)
                tasks.append((agent_key, task))
            
            # Execute all agents concurrently
            logger.info("Executing 5 concurrent API calls to Bedrock")
            concurrent_results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
            
            # Aggregate results
            agent_results = {}
            for i, (agent_key, _) in enumerate(tasks):
                result = concurrent_results[i]
                
                if isinstance(result, Exception):
                    logger.error(f"Agent {agent_key} failed with exception: {str(result)}")
                    # Create fallback result for failed agent
                    agent_results[agent_key] = {
                        "agent_name": self.agents[agent_key].name,
                        "score": 0.5,
                        "flag_type": "medium-risk",
                        "violations": ["processing_exception"],
                        "reasoning": f"Agent failed with exception: {str(result)}",
                        "specific_findings": ["Agent processing exception occurred"],
                        "recommendations": ["Retry request", "Check system status"]
                    }
                else:
                    agent_results[agent_key] = result
            
            successful_agents = sum(1 for result in agent_results.values() 
                                  if "processing_error" not in result.get("violations", []) 
                                  and "processing_exception" not in result.get("violations", []))
            
            logger.info(f"Concurrent processing completed. {successful_agents}/5 agents successful")
            return agent_results
            
        except Exception as e:
            logger.error(f"Concurrent processing failed: {str(e)}")
            
            # Return error results for all agents
            error_results = {}
            for agent_key, agent in self.agents.items():
                error_results[agent_key] = {
                    "agent_name": agent.name,
                    "score": 0.5,
                    "flag_type": "medium-risk",
                    "violations": ["concurrent_processing_error"],
                    "reasoning": f"Concurrent processing failed: {str(e)}",
                    "specific_findings": ["Concurrent processing error occurred"],
                    "recommendations": ["Retry request", "Check system status"]
                }
            
            return error_results
    
    def get_agent_info(self) -> Dict[str, str]:
        """
        Get information about all available agents
        """
        return {
            agent_key: agent.name 
            for agent_key, agent in self.agents.items()
        }
