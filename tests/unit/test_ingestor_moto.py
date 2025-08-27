import json, os, uuid
from moto import mock_aws
import boto3

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_ingestor_logic():
    # Fakes
    ddb = boto3.resource("dynamodb")
    sns = boto3.client("sns")
    table = ddb.create_table(
        TableName="events",
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
    )
    topic_arn = sns.create_topic(Name="events-topic")["TopicArn"]

    os.environ["TABLE_NAME"] = "events"
    os.environ["TOPIC_ARN"] = topic_arn

    from src.ingestor.app import handler

    s3_event = {
        "Records": [{
            "s3": {"object": {"key": "file.txt"}}
        }]
    }
    resp = handler(s3_event, None)
    assert resp["ok"]
    # 1 item en DDB
    items = table.scan()["Items"]
    assert len(items) == 1
