import boto3
bucket = input("Please input bucket name you would like to delete: ")
try:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    bucket.object_versions.delete()
except s3.exceptions.keyerror:
    print("That is not a valid bucket.")
confirm_delete_bucket = input("Would you also like to delete bucket:{bucket}: ")
if confirm_delete_bucket == "y":
    bucket.delete()
else:
    exit()