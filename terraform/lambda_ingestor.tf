data "archive_file" "ingestor_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/ingestor"
  output_path = "${path.module}/../build/ingestor.zip"
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda-basic-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "lambda_inline" {
  name = "lambda-inline"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect="Allow", Action=["logs:*"], Resource="*" },
      { Effect="Allow", Action=["dynamodb:*"], Resource=aws_dynamodb_table.events.arn },
      { Effect="Allow", Action=["sns:*"], Resource=aws_sns_topic.events.arn },
      { Effect="Allow", Action=["s3:*"], Resource="*" }
    ]
  })
}

resource "aws_lambda_function" "ingestor" {
  function_name    = "ingestor"
  filename         = data.archive_file.ingestor_zip.output_path
  source_code_hash = data.archive_file.ingestor_zip.output_base64sha256
  handler          = "app.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_role.arn
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.events.name
      TOPIC_ARN  = aws_sns_topic.events.arn
      AWS_DEFAULT_REGION = "us-east-1"
    }
  }
}
