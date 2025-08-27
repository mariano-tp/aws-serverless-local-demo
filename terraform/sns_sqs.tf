# Cola creada por CLI (ver job de CI). Aquí solo la LEEMOS.
data "aws_sqs_queue" "events" {
  name = "events-queue"
}

resource "aws_sns_topic" "events" {
  name = "events-topic"
}

# Permiso para que SNS pueda enviar a la cola
resource "aws_sqs_queue_policy" "allow_sns" {
  queue_url = data.aws_sqs_queue.events.url
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "sns.amazonaws.com" },
      Action    = "SQS:SendMessage",
      Resource  = data.aws_sqs_queue.events.arn,
      Condition = {
        ArnEquals = { "aws:SourceArn" = aws_sns_topic.events.arn }
      }
    }]
  })
}

resource "aws_sns_topic_subscription" "sqs_sub" {
  topic_arn = aws_sns_topic.events.arn
  protocol  = "sqs"
  endpoint  = data.aws_sqs_queue.events.arn

  depends_on = [aws_sqs_queue_policy.allow_sns]
}
