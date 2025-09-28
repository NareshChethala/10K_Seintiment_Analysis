from scripts.config import S3_BUCKET_NAME
import boto3

def upload_file_to_s3(file_path, bucket_name=S3_BUCKET_NAME, s3_key=None):
    s3 = boto3.client("s3")
    if s3_key is None:
        s3_key = os.path.basename(file_path)
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"✅ Uploaded {file_path} to s3://{bucket_name}/{s3_key}")