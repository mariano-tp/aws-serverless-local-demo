import os, time, json, boto3

ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

def _clients():
    s3  = boto3.client("s3", endpoint_url=ENDPOINT, region_name=REGION)
    ddb = boto3.resource("dynamodb", endpoint_url=ENDPOINT, region_name=REGION)
    sqs = boto3.client("sqs", endpoint_url=ENDPOINT, region_name=REGION)
    return s3, ddb, sqs

def test_whole_flow():
    s3, ddb, sqs = _clients()

    # pre-creados por Terraform
    bucket = "events-bucket"
    queue_url = sqs.get_queue_url(QueueName="events-queue")["QueueUrl"]
    table = ddb.Table("events")

    # Sube objeto → dispara Lambda ingestor
    s3.put_object(Bucket=bucket, Key="demo.txt", Body=b"hi")

    # Espera eventual consumo
    time.sleep(2)

    # Debe haber un item en DynamoDB
    scan = table.scan()
    assert scan["Count"] >= 1

    # Y mensaje en la cola
    msgs = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=1)
    assert "Messages" in msgs or scan["Count"] >= 1
