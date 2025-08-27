import os
import uuid
import boto3

TABLE = os.getenv("TABLE_NAME", "events")
ddb = boto3.resource("dynamodb", region_name="us-east-1")
table = ddb.Table(TABLE)

def lambda_handler(event, context):
    """
    Procesa eventos de S3 recibidos via SQS (S3->SQS->Lambda).
    Escribe un item (id,bucket,key) en DynamoDB.
    """
    for rec in event.get("Records", []):
        s3 = rec.get("s3") or {}
        bucket = (s3.get("bucket") or {}).get("name")
        key = (s3.get("object") or {}).get("key")

        table.put_item(
            Item={
                "id": str(uuid.uuid4()),
                "bucket": bucket or "unknown",
                "key": key or "unknown",
            }
        )
    return {"ok": True}
