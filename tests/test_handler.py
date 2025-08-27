import os
import json
import boto3
import pytest
from moto import mock_aws
from app import handler


@pytest.fixture(autouse=True)
def mock_dynamo_env(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("TABLE_NAME", "TodosTable")


@mock_aws
def test_create_and_get_todo():
    # Crear tabla mock (moto)
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName="TodosTable",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # POST /todos
    evt_post = {
        "body": json.dumps({"id": "1", "title": "demo"}),
        "httpMethod": "POST",
        "path": "/todos",
    }
    resp_post = handler.create_todo(evt_post, None)
    assert resp_post["statusCode"] == 201

    # GET /todos/1
    evt_get = {"httpMethod": "GET", "pathParameters": {"id": "1"}, "path": "/todos/1"}
    resp_get = handler.get_todo(evt_get, None)
    assert resp_get["statusCode"] == 200
    body = json.loads(resp_get["body"])
    assert body["item"]["id"] == "1"
    assert body["item"]["title"] == "demo"
