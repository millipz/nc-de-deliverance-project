resource "aws_scheduler_schedule" "etl_schedule" {
  name       = "${var.env_name}-ETL-Schedule"
  

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(10 minutes)"

  target {
    arn      = aws_sfn_state_machine.nc-totesys-deliverance.arn
    role_arn = aws_iam_role.eventbridge_schedule_policy_exec_role.arn
  }
}

resource "aws_lambda_permission" "allow_eventbridge" {
    statement_id = "AllowExecutionFromEventBridge"
    action = "lambda:InvokeFunction"
    principal = "events.amazonaws.com"
    function_name = aws_lambda_function.ingestion_function.function_name
}

resource "aws_cloudwatch_log_group" "ingestion_lambda_log_group" {
   name = "/aws/lambda/${var.env_name}-ingestion-function"
}

resource "aws_cloudwatch_log_metric_filter" "ingestion_lambda_log_metric_filter" {
  depends_on = [ aws_lambda_function.ingestion_function ]
  name = "${var.env_name}-ingestion_lambda_log_metric_filter"
  pattern = "Error"
  log_group_name = "/aws/lambda/${var.env_name}-ingestion-function"
  metric_transformation {
    name = "${var.env_name}-ingestion_lambda_warning"
    namespace = "ingestion_warnings"
    value = 1
  }
}

resource "aws_cloudwatch_metric_alarm" "ingestion_lambda_error_alarm" {
  alarm_name          = "${var.env_name}-ingestion-lambda_error_alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "${var.env_name}-ingestion_lambda_warning"
  namespace           = "ingestion_warnings"
  period              = 900
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm when the Lambda function errors"
  alarm_actions       = [aws_sns_topic.lambda_failure_topic.arn]
}


# Processing

resource "aws_cloudwatch_log_group" "processing_lambda_log_group" {
   name = "/aws/lambda/${var.env_name}-processing-function"
}

resource "aws_cloudwatch_log_metric_filter" "processing_lambda_log_metric_filter" {
  depends_on = [ aws_lambda_function.processing_function ]
  name = "${var.env_name}-processing_lambda_log_metric_filter"
  pattern = "Error"
  log_group_name = "/aws/lambda/${var.env_name}-processing-function"
  metric_transformation {
    name = "${var.env_name}-processing_lambda_warning"
    namespace = "processing_warnings"
    value = 1
  }
}

resource "aws_cloudwatch_metric_alarm" "processing_lambda_error_alarm" {
  alarm_name          = "${var.env_name}-processing-lambda_error_alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "${var.env_name}-processing_lambda_warning"
  namespace           = "processing_warnings"
  period              = 900
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm when the Lambda function errors"
  alarm_actions       = [aws_sns_topic.lambda_failure_topic.arn]
}

# Loading

resource "aws_cloudwatch_log_group" "loading_lambda_log_group" {
   name = "/aws/lambda/${var.env_name}-loading-function"
}

resource "aws_cloudwatch_log_metric_filter" "loading_lambda_log_metric_filter" {
  depends_on = [ aws_lambda_function.loading_function ]
  name = "${var.env_name}-loading_lambda_log_metric_filter"
  pattern = "Error"
  log_group_name = "/aws/lambda/${var.env_name}-loading-function"
  metric_transformation {
    name = "${var.env_name}-loading_lambda_warning"
    namespace = "loading_warnings"
    value = 1
  }
}

resource "aws_cloudwatch_metric_alarm" "loading_lambda_error_alarm" {
  alarm_name          = "${var.env_name}-loading-lambda_error_alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "${var.env_name}-loading_lambda_warning"
  namespace           = "loading_warnings"
  period              = 900
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alarm when the Lambda function errors"
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
