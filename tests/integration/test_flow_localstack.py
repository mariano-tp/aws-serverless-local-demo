import time
import boto3
import os

ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

def _clients():
    s3 = boto3.client("s3", endpoint_url=ENDPOINT, region_name=REGION)
    sqs = boto3.client("sqs", endpoint_url=ENDPOINT, region_name=REGION)
    ddb = boto3.resource("dynamodb", endpoint_url=ENDPOINT, region_name=REGION)
    return s3, ddb, sqs

def test_whole_flow():
    s3, ddb, sqs = _clients()

    bucket = "events-bucket"
    queue_url = sqs.get_queue_url(QueueName="events-queue")["QueueUrl"]
    table = ddb.Table("events")

    # Dispara evento
    s3.put_object(Bucket=bucket, Key="demo.txt", Body=b"hi")

    # Poll DDB hasta 30s
    deadline = time.time() + 30
    seen = 0
    while time.time() < deadline:
        scan = table.scan()
        seen = scan.get("Count", 0)
        if seen >= 1:
            break
        time.sleep(1)

    assert seen >= 1
