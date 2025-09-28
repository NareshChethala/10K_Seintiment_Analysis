# scripts/clean_and_upload_filings.py

import boto3
from botocore.exceptions import ClientError
from scripts.clean_filing_html import clean_filing_html

def list_raw_html_keys(s3_client, bucket, prefix):
    """List raw filing HTMLs from S3."""
    keys = []
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".html"):
                keys.append(obj["Key"])
    return keys


def clean_and_upload(bucket, input_prefix="raw_filings/", output_prefix="cleaned_filings/", limit=None):
    """
    Downloads raw HTML filings from S3, cleans them, and uploads cleaned text back to S3.
    
    Args:
        bucket (str): S3 bucket name.
        input_prefix (str): Folder where raw HTML files are stored.
        output_prefix (str): Folder where cleaned text will be saved.
        limit (int): Optional limit on number of files to process.
    """
    s3 = boto3.client("s3")
    processed = 0

    raw_keys = list_raw_html_keys(s3, bucket, input_prefix)
    print(f"🔍 Found {len(raw_keys)} raw HTML files in s3://{bucket}/{input_prefix}")

    for raw_key in raw_keys:
        if limit and processed >= limit:
            break

        output_key = output_prefix + raw_key.split("/")[-1].replace(".html", ".txt")

        # Skip if already cleaned
        try:
            s3.head_object(Bucket=bucket, Key=output_key)
            print(f"🔁 Already cleaned: {output_key}")
            continue
        except ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise

        # Download raw HTML
        response = s3.get_object(Bucket=bucket, Key=raw_key)
        html = response["Body"].read().decode("utf-8")

        # Clean
        cleaned_text = clean_filing_html(html)
        if not cleaned_text.strip():
            print(f"⚠️ No usable text from: {raw_key}")
            continue

        # Upload cleaned text
        s3.put_object(Bucket=bucket, Key=output_key, Body=cleaned_text)
        print(f"✅ Cleaned and uploaded: s3://{bucket}/{output_key}")
        processed += 1