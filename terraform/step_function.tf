resource "aws_sfn_state_machine" "nc-totesys-deliverance" {
  name     = "${var.env_name}-nc-totesys-deliverance"
  role_arn = aws_iam_role.step_function_policy_exec_role.arn

  definition = data.template_file.step-function-template.rendered
}