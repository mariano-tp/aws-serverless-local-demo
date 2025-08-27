import json
import os
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.getenv("TABLE_NAME", "TodosTable")
REGION = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


def _response(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def create_todo(event, context):
    """POST /todos  -> body: {"id": "1", "title": "algo"}"""
    try:
        payload = json.loads(event.get("body") or "{}")
        item = {"id": payload["id"], "title": payload.get("title", "")}
        table.put_item(Item=item)
        return _response(201, {"ok": True, "item": item})
    except Exception as e:
        return _response(400, {"ok": False, "error": str(e)})


def get_todo(event, context):
    """GET /todos/{id}"""
    todo_id = event.get("pathParameters", {}).get("id")
    if not todo_id:
        return _response(400, {"ok": False, "error": "missing id"})

    res = table.get_item(Key={"id": todo_id})
    item = res.get("Item")
    if not item:
        return _response(404, {"ok": False, "error": "not found"})
    return _response(200, {"ok": True, "item": item})
