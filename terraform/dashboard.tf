resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.env_name}-dashboard"
  dashboard_body = data.template_file.dashboard.rendered
}