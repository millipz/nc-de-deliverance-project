resource "aws_cloudwatch_event_rule" "ingestion_schedule" {
    name = "ingestion_schedule"
    description = "Eventbridge rule to trigger ingestion Lambda function every 10 minutes"
    schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "ingestion_lambda_target" {
    rule = aws_cloudwatch_event_rule.ingestion_schedule.name
    target_id = "ingestion_lambda_target"
    arn = aws_lambda_function.ingestion_function.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
    statement_id = "AllowExecutionFromEventBridge"
    action = "lambda:InvokeFunction"
    principal = "events.amazonaws.com"
    function_name = aws_lambda_function.ingestion_function.function_name
}


resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "lambda_error_alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 900
  statistic           = "Sum"
  threshold           = 2
  alarm_description   = "Alarm when the Lambda function errors more than 2 times in a minute"
  alarm_actions       = [aws_sns_topic.lambda_failure_topic.arn]

  dimensions = {
    FunctionName = aws_lambda_function.ingestion_function.name
  }
}

resource "aws_sns_topic" "lambda_failure_topic" {
  name = "lambda_failure_topic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.lambda_failure_topic.arn
  protocol  = "email"
  endpoint  = "oliverjohnboyd@gmail.com"
}

resource "aws_cloudwatch_event_target" "send_sns" {
  rule      = aws_cloudwatch_event_rule.alarm_state_change.name
  arn       = aws_sns_topic.lambda_failure_topic.arn
}