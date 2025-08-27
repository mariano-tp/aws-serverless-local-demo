import os
import time
import boto3


def _clients():
    endpoint = os.environ.get("LOCALSTACK_ENDPOINT", "http://localhost:4566")
    session = boto3.session.Session(region_name="us-east-1")
    s3 = session.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    sqs = session.client(
        "sqs",
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    ddb = session.resource(
        "dynamodb",
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    return s3, ddb, sqs


def test_whole_flow():
    s3, ddb, sqs = _clients()

    # Recursos pre-creados por el workflow
    bucket = "events-bucket"
    queue_url = sqs.get_queue_url(QueueName="events-queue")["QueueUrl"]
    table = ddb.Table("events")

    # 1) Subimos un objeto a S3 -> S3 emite evento hacia SQS
    s3.put_object(Bucket=bucket, Key="demo.txt", Body=b"hi")

    # 2) Consumimos UN mensaje de la queue y al "procesarlo" escribimos en DynamoDB
    found = False
    for _ in range(15):  # ~15s max
        resp = sqs.receive_message(
            QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=1
        )
        msgs = resp.get("Messages", [])
        if msgs:
            # Simulamos lógica de Lambda: al consumir, persistimos algo en DDB
            table.put_item(Item={"pk": "s3#demo.txt", "sk": str(int(time.time()))})
            # limpiamos el mensaje
            for m in msgs:
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=m["ReceiptHandle"])
            found = True
            break
        time.sleep(1)

    assert found, "No se recibió ningún mensaje desde SQS (S3->SQS notification)"

    # 3) Verificamos que exista al menos 1 ítem en DDB
    scan = table.scan()
    assert scan["Count"] >= 1
