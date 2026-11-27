
from pydantic import BaseModel
from typing import Literal


class Evidence(BaseModel):
    comment_id: str
    comment_text: str


class Insight(BaseModel):
    insight_id: str
    title: str
    observation: str
    interpretation: str
    evidence: list[Evidence]
    business_impact: str
    confidence: Literal["low", "medium", "high"]


class Recommendation(BaseModel):
    recommendation_id: str
    title: str
    action: str
    reason: str
    priority: Literal["low", "medium", "high"]
    related_insights: list[str]
    expected_benefit: str
    human_decision: Literal["pending", "approved", "rejected", "edited"] = "pending"


class Opportunity(BaseModel):
    title: str
    description: str
    supporting_evidence: list[str]


class AgentResponse(BaseModel):
    executive_summary: str
    key_insights: list[Insight]
    recommendations: list[Recommendation]
    opportunities: list[Opportunity]
    data_limitations: list[str]
    human_review_required: bool = True



def validate_evidence_ids(response, available_comment_ids):
    available_ids = set(available_comment_ids)
    invalide_ids=[]

    for insight in response.key_insights:
        for evidence in insight.evidence:
            if evidence.comment_id not in available_ids:
                invalide_ids.append(evidence.comment_id)

    for opportunity in response.opportunities:
        for comment_id in opportunity.supporting_evidence:
            if comment_id not in available_ids:
                invalide_ids.append(comment_id)

    if invalide_ids:
        raise ValueError(f"Invalid comment IDs found: {invalide_ids}")

    return True



def validate_evidence_content(response, comments_by_id):
    for insight in response.key_insights:
        for evidence in insight.evidence:
            original_text = comments_by_id.get(evidence.comment_id)
            if original_text is None:
                raise ValueError(f"Unknown comment ID: {evidence.comment_id}")
            if evidence.comment_text != original_text:
                raise ValueError(f"Evidence text mismatch for {evidence.comment_id}")
            return True