resource "aws_s3_bucket" "events" {
  bucket = "events-bucket"
}

resource "aws_s3_bucket_notification" "to_sqs" {
  bucket = aws_s3_bucket.events.id

  queue {
    queue_arn = aws_sqs_queue.events.arn
    events    = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_sqs_queue_policy.allow_s3]
}
