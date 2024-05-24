import boto3

env = input("Please input the environment name for which to delete parameters: ")
c = boto3.client("ssm")
param_names = [
    param["Name"]
    for param in c.describe_parameters(
        ParameterFilters=[
            {
                "Key": "Name",
                "Option": "BeginsWith",
                "Values": [env],
            }
        ]
    )["Parameters"]
]

if len(param_names):
    print(f"About to delete {param_names}")
    confirm_delete = input("Are you sure you wish to delete these parameters: ")
    if confirm_delete == "y":
        for name in param_names:
            print(f"deleting {name} ...")
            c.delete_parameter(Name=name)
else:
    print(f"No parameters found for {env} environment")


# try:
#     s3 = boto3.resource("s3")
#     bucket = s3.Bucket(bucket)
#     bucket.object_versions.delete()
# except s3.exceptions.keyerror:
#     print("That is not a valid bucket.")
# confirm_delete_bucket = input("Would you also like to delete bucket:f{bucket}: ")
# if confirm_delete_bucket == "y":
#     bucket.delete()
# else:
#     exit()
