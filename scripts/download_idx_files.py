import os
import time
import requests
from datetime import datetime
import boto3

BASE_URL = 'https://www.sec.gov/Archives/edgar/full-index/'

def download_file(url: str, path: str, headers: dict):
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def s3_file_exists(bucket: str, key: str) -> bool:
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except s3.exceptions.ClientError:
        return False

def upload_file_to_s3(local_path: str, bucket: str, s3_key: str):
    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket, s3_key)

def get_quarters_for_year(year: int, current_year: int, current_qtr: int):
    all_quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
    if year == current_year:
        return all_quarters[:current_qtr]
    return all_quarters

def download_idx_files_auto(save_dir: str, bucket: str, user_agent_email: str) -> int:
    os.makedirs(save_dir, exist_ok=True)
    headers = {"User-Agent": user_agent_email}
    new_files = 0

    now = datetime.now()
    current_year = now.year
    current_qtr = (now.month - 1) // 3 + 1

    for year in range(1993, current_year + 1):
        for qtr in get_quarters_for_year(year, current_year, current_qtr):
            filename = f"{year}_{qtr}_company.idx"
            local_path = os.path.join(save_dir, filename)
            s3_key = f"idx/{filename}"
            url = f"{BASE_URL}{year}/{qtr}/company.idx"

            # Skip if already in S3
            if s3_file_exists(bucket, s3_key):
                continue

            try:
                download_file(url, local_path, headers)
                upload_file_to_s3(local_path, bucket, s3_key)
                time.sleep(1)  # Politeness delay for SEC
                new_files += 1
            except Exception as e:
                print(f"Failed to download or upload {filename}: {e}")
                continue

    return new_files