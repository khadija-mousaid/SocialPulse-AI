
AGENT_OUTPUT_SCHEMA = {
    "executive_summary": "A concise overview of the most important findings",

    "key_insights": [
        {
            "insight_id": "INS001",
            "title": "Insight title",
            "observation": "What the data actually shows",
            "interpretation": "What this may mean for the business",
            "evidence": [
                {
                    "comment_id": "C001",
                    "comment_text": "Original source comment"
                }
            ],
            "business_impact": "Potential impact on the startup",
            "confidence": "low | medium | high"
        }
    ],

    "recommendations": [
        {
            "recommendation_id": "REC001",
            "title": "Recommendation title",
            "action": "Specific action to consider",
            "reason": "Why this action is suggested",
            "priority": "low | medium | high",
            "related_insights": ["INS001"],
            "expected_benefit": "Potential benefit",
            "human_decision": "pending"
        }
    ],

    "opportunities": [
        {
            "title": "Opportunity title",
            "description": "Potential business opportunity",
            "supporting_evidence": ["C001"]
        }
    ],

    "data_limitations": [
        "Known limitation affecting the analysis"
    ],

    "human_review_required": True
}
