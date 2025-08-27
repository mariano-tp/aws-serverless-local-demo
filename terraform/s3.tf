resource "aws_s3_bucket" "events" {
  bucket = "events-bucket"
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingestor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.events.arn
}

resource "aws_s3_bucket_notification" "notify" {
  bucket = aws_s3_bucket.events.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.ingestor.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}
