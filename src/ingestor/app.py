import json
import os
import boto3
import uuid

dynamodb = boto3.resource("dynamodb", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))
sns = boto3.client("sns", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))

TABLE = os.environ["TABLE_NAME"]
TOPIC_ARN = os.environ["TOPIC_ARN"]

def handler(event, context):
    # Evento S3 → toma key y genera un registro
    record = event["Records"][0]
    s3obj = record["s3"]["object"]["key"]
    item = {"id": str(uuid.uuid4()), "object_key": s3obj, "status": "RECEIVED"}

    table = dynamodb.Table(TABLE)
    table.put_item(Item=item)

    sns.publish(TopicArn=TOPIC_ARN, Message=json.dumps(item))
    return {"ok": True, "item": item}
