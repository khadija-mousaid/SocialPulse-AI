import json
from agent_schema import AGENT_OUTPUT_SCHEMA

#verifier que la structure peut etre convertie en JSON
schema_json = json.dumps(AGENT_OUTPUT_SCHEMA, ensure_ascii=False, indent=4)

print("Schema JSON valide !")
print(schema_json)