# Terraform

## Justification

We will use Terraform to manage and deploy our infrastructure, to ensure all assets (buckets, lambda functions, eventbridge triggers, permissions) are cleanly managed and reproduceable. By tracking state with Terraform we can also easily tear down and rebuild the infrastructure if necessary