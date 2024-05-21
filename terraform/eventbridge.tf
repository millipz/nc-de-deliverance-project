resource "aws_cloudwatch_event_rule" "ingestion_schedule" {
    name = "${var.env_name}-ingestion_schedule"
    description = "Eventbridge rule to trigger ingestion Lambda function every 10 minutes"
    schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "ingestion_lambda_target" {
    rule = aws_cloudwatch_event_rule.ingestion_schedule.name
    target_id = "${var.env_name}-ingestion_lambda_target"
    arn = aws_lambda_function.ingestion_function.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
    statement_id = "AllowExecutionFromEventBridge"
    action = "lambda:InvokeFunction"
    principal = "events.amazonaws.com"
    function_name = aws_lambda_function.ingestion_function.function_name
}

resource "aws_cloudwatch_log_metric_filter" "ingestion_lambda_log_metric_filter" {
  depends_on = [ aws_cloudwatch_log_group.ingestion_lambda_log_group ]
  name = "${var.env_name}-ingestion_lambda_log_metric_filter"
  pattern = "Error"
  log_group_name = "/aws/lambda/${var.env_name}-ingestion-function"
  metric_transformation {
    name = "${var.env_name}-ingestion_lambda_warning"
    namespace = "ingestion_warnings"
    value = 1
  }
}

resource "aws_cloudwatch_log_group" "ingestion_lambda_log_group" {
  name = "/aws/lambda/${var.env_name}-ingestion-function"
}

resource "aws_cloudwatch_metric_alarm" "ingestion_lambda_error_alarm" {
  alarm_name          = "${var.env_name}-lambda_error_alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "ingestion_warnings"
  period              = 900
  statistic           = "Sum"
  threshold           = 2
  alarm_description   = "Alarm when the Lambda function errors more than 2 times in a minute"
  alarm_actions       = [aws_sns_topic.lambda_failure_topic.arn]
}

resource "aws_sns_topic" "lambda_failure_topic" {
  name = "${var.env_name}-lambda_failure_topic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.lambda_failure_topic.arn
  protocol  = "email"
  endpoint  = var.admin_email
}
