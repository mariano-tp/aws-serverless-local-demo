# src/handler.py
import os, uuid, boto3

TABLE = os.getenv("TABLE_NAME", "events")
ddb = boto3.resource("dynamodb", region_name="us-east-1")
table = ddb.Table(TABLE)

def lambda_handler(event, context):
    # Parsea eventos S3 desde SQS (formato Records[])
    for r in event.get("Records", []):
        s3 = r.get("s3") or {}
        bucket = (s3.get("bucket") or {}).get("name")
        key = (s3.get("object") or {}).get("key")
        table.put_item(Item={"id": str(uuid.uuid4()), "bucket": bucket or "unknown", "key": key or "unknown"})
    return {"ok": True}
