resource "aws_sns_topic" "events" {
  name = "events-topic"
}

resource "aws_sqs_queue" "events" {
  name = "events-queue"
}

resource "aws_sns_topic_subscription" "sqs_sub" {
  topic_arn = aws_sns_topic.events.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.events.arn
}
