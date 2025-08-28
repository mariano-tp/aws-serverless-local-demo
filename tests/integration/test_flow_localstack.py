import os
import time
import uuid
import boto3


ENDPOINT = os.environ.get("LOCALSTACK_ENDPOINT", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def clients():
    s3 = boto3.client("s3", endpoint_url=ENDPOINT, region_name=REGION,
                      aws_access_key_id="test", aws_secret_access_key="test")
    sqs = boto3.client("sqs", endpoint_url=ENDPOINT, region_name=REGION,
                       aws_access_key_id="test", aws_secret_access_key="test")
    ddb = boto3.client("dynamodb", endpoint_url=ENDPOINT, region_name=REGION,
                       aws_access_key_id="test", aws_secret_access_key="test")
    return s3, sqs, ddb


def test_whole_flow():
    s3, sqs, ddb = clients()

    bucket = "events-bucket"
    queue_url = sqs.get_queue_url(QueueName="events-queue")["QueueUrl"]

    # 1) Evento en S3
    key = f"demo-{uuid.uuid4().hex}.txt"
    s3.put_object(Bucket=bucket, Key=key, Body=b"hello")

    # 2) Recibo notificación en SQS (LocalStack simula S3->SQS)
    msg = None
    deadline = time.time() + 30
    while time.time() < deadline:
        resp = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=2)
        messages = resp.get("Messages", [])
        if messages:
            msg = messages[0]
            # 3) Simulo un worker que persiste en DynamoDB
            ddb.put_item(
                TableName="events",
                Item={
                    "id": {"S": uuid.uuid4().hex},
                    "key": {"S": key},
                    "ts": {"S": str(int(time.time()))},
                },
            )
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"])
            break

    # 4) Valido que haya al menos un registro en DDB
    scan = ddb.scan(TableName="events")
    assert scan.get("Count", 0) >= 1
