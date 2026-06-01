from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GovernanceRequest(BaseModel):
    llm_output: str = Field(..., description="The LLM output to analyze for compliance")
    client_id: Optional[str] = Field(None, description="Optional client identifier for tracking")

class AgentResult(BaseModel):
    agent_name: str = Field(..., description="Name of the compliance agent")
    score: float = Field(..., ge=0.0, le=1.0, description="Compliance score from 0.0 to 1.0")
    flag_type: str = Field(..., description="Risk level: none, low-risk, medium-risk, high-risk")
    violations: List[str] = Field(default=[], description="List of specific violations found")
    reasoning: str = Field(..., description="Detailed explanation of the score and violations")
    specific_findings: List[str] = Field(default=[], description="Specific issues identified in the content")
    recommendations: List[str] = Field(default=[], description="Actionable recommendations to address violations")

class ExecutiveSummary(BaseModel):
    total_agents: int = Field(default=5, description="Total number of agents analyzed")
    agents_with_violations: int = Field(..., description="Number of agents that found violations")
    highest_risk_agent: str = Field(..., description="Agent with the lowest compliance score")
    lowest_score: float = Field(..., description="Lowest compliance score across all agents")
    critical_violations: List[str] = Field(default=[], description="Most critical violations found")
    immediate_actions_required: List[str] = Field(default=[], description="Actions that need immediate attention")

class KeyConcern(BaseModel):
    area: str = Field(..., description="Compliance area with concerns")
    issue: str = Field(..., description="Specific issue identified")
    severity: str = Field(..., description="Severity level of the issue")
    impact: str = Field(..., description="Potential impact of the issue")

class ClientSummary(BaseModel):
    compliance_status: str = Field(..., description="Overall compliance status")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence in the analysis")
    key_concerns: List[KeyConcern] = Field(default=[], description="Key areas of concern")
    priority_actions: List[str] = Field(default=[], description="Priority actions to take")
    regulatory_implications: List[str] = Field(default=[], description="Potential regulatory implications")
    business_impact: str = Field(..., description="Overall business impact assessment")

class ViolationCategory(BaseModel):
    count: int = Field(..., description="Number of times this violation occurred")
    agents: List[str] = Field(..., description="Agents that identified this violation")
    severity: str = Field(..., description="Severity level of this violation type")
    description: str = Field(..., description="Description of what this violation means")

class ViolationAnalysis(BaseModel):
    by_category: Dict[str, ViolationCategory] = Field(default={}, description="Violations grouped by category")
    severity_breakdown: Dict[str, int] = Field(default={"high": 0, "medium": 0, "low": 0}, description="Count of violations by severity")
    compliance_gaps: List[str] = Field(default=[], description="Identified compliance gaps")

class RecommendationsSummary(BaseModel):
    immediate: List[str] = Field(default=[], description="Actions needed immediately")
    short_term: List[str] = Field(default=[], description="Actions needed in the short term")
    long_term: List[str] = Field(default=[], description="Long-term strategic actions")

class AgentDetail(BaseModel):
    compliance_score: float = Field(..., description="Agent's compliance score")
    risk_level: str = Field(..., description="Risk level determined by agent")
    violations_found: int = Field(..., description="Number of violations found")
    specific_issues: List[str] = Field(default=[], description="Specific issues identified")
    why_this_score: str = Field(..., description="Explanation of why this score was given")
    what_to_fix: List[str] = Field(default=[], description="What needs to be fixed")
    regulatory_impact: str = Field(..., description="Potential regulatory impact")

class DetailedBreakdown(BaseModel):
    executive_summary: ExecutiveSummary = Field(..., description="High-level executive summary")
    agent_details: Dict[str, AgentDetail] = Field(default={}, description="Detailed breakdown by agent")
    violation_analysis: ViolationAnalysis = Field(..., description="Analysis of violations found")
    recommendations_summary: RecommendationsSummary = Field(..., description="Summary of recommendations")

class GovernanceResponse(BaseModel):
    original_output: str = Field(..., description="The original LLM output that was analyzed")
    governance_results: Dict[str, AgentResult] = Field(..., description="Results from each compliance agent")

    class Config:
        json_schema_extra = {
            "example": {
                "original_output": "Hello, my email is john@example.com",
                "governance_results": {
                    "data_privacy_security": {
                        "agent_name": "Data Privacy & Security",
                        "score": 0.6,
                        "flag_type": "medium-risk",
                        "violations": ["pii_exposure"],
                        "reasoning": "Email address detected without proper consent mechanisms",
                        "specific_findings": ["Email 'john@example.com' exposed without consent"],
                        "recommendations": ["Remove or pseudonymize email addresses"]
                    },
                    "ai_risk_ethics": {
                        "agent_name": "AI Risk & Ethics",
                        "score": 0.9,
                        "flag_type": "none",
                        "violations": [],
                        "reasoning": "No ethical concerns detected in simple greeting",
                        "specific_findings": [],
                        "recommendations": []
                    },
                    "content_platform": {
                        "agent_name": "Content & Platform Compliance",
                        "score": 0.9,
                        "flag_type": "none",
                        "violations": [],
                        "reasoning": "Content is safe and appropriate",
                        "specific_findings": [],
                        "recommendations": []
                    },
                    "standards_quality": {
                        "agent_name": "Standards & Quality",
                        "score": 0.8,
                        "flag_type": "none",
                        "violations": [],
                        "reasoning": "Content meets quality standards",
                        "specific_findings": [],
                        "recommendations": []
                    },
                    "legal_regulatory": {
                        "agent_name": "Legal & Regulatory",
                        "score": 0.9,
                        "flag_type": "none",
                        "violations": [],
                        "reasoning": "No legal risks identified",
                        "specific_findings": [],
                        "recommendations": []
                    }
                }
            }
        }
