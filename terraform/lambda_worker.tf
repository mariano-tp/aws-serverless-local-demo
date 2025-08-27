data "archive_file" "worker_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src/worker"
  output_path = "${path.module}/../build/worker.zip"
}

resource "aws_lambda_function" "worker" {
  function_name    = "worker"
  filename         = data.archive_file.worker_zip.output_path
  source_code_hash = data.archive_file.worker_zip.output_base64sha256
  handler          = "app.handler"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_role.arn
}

resource "aws_lambda_event_source_mapping" "sqs_to_worker" {
  event_source_arn = aws_sqs_queue.events.arn
  function_name    = aws_lambda_function.worker.arn
  batch_size       = 1
}
