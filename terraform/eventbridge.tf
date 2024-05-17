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