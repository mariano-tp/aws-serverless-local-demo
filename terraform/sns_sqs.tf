resource "aws_sqs_queue" "events" {
  name = "events-queue"
}

resource "aws_sqs_queue_policy" "allow_s3" {
  queue_url = aws_sqs_queue.events.id
  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = { Service = "s3.amazonaws.com" },
        Action    = "SQS:SendMessage",
        Resource  = aws_sqs_queue.events.arn,
        Condition = {
          ArnEquals = {
            "aws:SourceArn" = aws_s3_bucket.events.arn
          }
        }
      }
    ]
  })
}
