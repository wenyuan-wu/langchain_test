import json

json_str = """
        {
        "reason_found": false,
        "reason": null,
        "confidence_score": 0
        }
"""

print(json_str)

json_obj = json.loads(json_str)
print(json_obj)
