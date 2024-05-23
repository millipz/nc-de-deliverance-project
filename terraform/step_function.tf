resource "aws_sfn_state_machine" "nc-totesys-deliverance" {
  name     = "nc-totesys-deliverance"
  role_arn = "arn:aws:iam::471112858444:role/service-role/StepFunctions-MyStateMachine-em9sr6pes-role-moutpkww6"

  definition = file("step_function.json")
}