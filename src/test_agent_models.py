import pandas as pd
from agent_models import AgentResponse, validate_evidence_ids, validate_evidence_content
import json

# Exemple de réponse fictive de l'agent
sample_response = {
    "executive_summary": "Delivery issues need further investigation.",

    "key_insights": [
        {
            "insight_id": "INS001",
            "title": "Delivery delays",
            "observation": "Some comments mention late delivery.",
            "interpretation": "Delivery reliability may need improvement.",
            "evidence": [
                {
                    "comment_id": "C002",
                    "comment_text": "Livraison arrivée avec 40 minutes de retard aujourd'hui."
                }
            ],
            "business_impact": "Potential reduction in customer satisfaction.",
            "confidence": "medium"
        }
    ],

    "recommendations": [
        {
            "recommendation_id": "REC001",
            "title": "Monitor delivery delays",
            "action": "Track delivery times and investigate delays.",
            "reason": "Several comments mention delivery problems.",
            "priority": "medium",
            "related_insights": ["INS001"],
            "expected_benefit": "Improved delivery reliability.",
            "human_decision": "pending"
        }
    ],

    "opportunities": [],

    "data_limitations": [
        "The dataset contains synthetic comments."
    ],

    "human_review_required": True
}

# Valider la réponse
validated_response = AgentResponse.model_validate(sample_response)

#charger les IDs disponibles dans le dataset
with open("data/agent_context.json", "r", encoding="utf-8") as file:
    context = json.load(file)

available_ids = context["metadata"]["available_comment_ids"]

#tester les preuves
validate_evidence_ids(validated_response, available_ids)

print("Evidence IDs are valid!")

#tester un ID inexistant
invalid_data = validated_response.model_dump()

invalid_data["key_insights"][0]["evidence"][0]["comment_id"]="C99"

invalid_response = AgentResponse.model_validate(invalid_data)

try:
    validate_evidence_ids(invalid_response, available_ids)
    print("ERROR: Invalid ID was not detected!")

except ValueError as error:
    print("Invalid ID detected successfully !")
    print(error)


#charger les commentaires originaux
comments_df = pd.read_csv("data/socialpulse_comments_synthetic.csv")
comment_by_id = dict(zip(comments_df["comment_id"], comments_df["comment_text"]))

#verifier que le texte des preuves est exact
validate_evidence_content(validated_response, comment_by_id)

print("Evidence content is valid!")



#simuler une preuve avec un texte invente
fake_data= validated_response.model_dump()

fake_data["key_insights"][0]["evidence"][0]["comment_text"]=("La livraison est toujours en retard.")

fake_response = AgentResponse.model_validate(fake_data)

try:
    validate_evidence_content(fake_response, comment_by_id)
    print("ERROR: Fake evidence was not detected!")

except ValueError as error:
    print("Fake evidence detected successfully!")
    print(error)


print("Agent response is valid!")
print(validated_response.model_dump_json(indent=4))
