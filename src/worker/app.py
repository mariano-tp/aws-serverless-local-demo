import os
import json
import boto3

def handler(event, context):
    # Mensajes de SQS (publicados por SNS) → loguea o “procesa”
    for r in event.get("Records", []):
        body = json.loads(r["body"])
        # LocalStack enruta SNS→SQS con el mensaje original bajo "Message"
        msg = json.loads(body.get("Message", "{}"))
        print("WORKER got:", msg)
    return {"ok": True}
