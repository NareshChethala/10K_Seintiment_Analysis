import requests
import pandas as pd
from bs4 import BeautifulSoup
import boto3
import os

def extract_filing_html_directly(row, user_agent_email):
    try:
        filename = row['Filename'].strip().replace(" ", "")
        path_parts = filename.split("/")

        if len(path_parts) < 4:
            print(f"Invalid path in Filename: {filename}")
            return None, None, None

        cik = path_parts[2]
        accession_with_dashes = path_parts[3]
        accession_nodashes = accession_with_dashes.replace("-", "")
        index_filename = accession_with_dashes + "-index.htm"

        index_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodashes}/{index_filename}"
        headers = {"User-Agent": user_agent_email}

        response = requests.get(index_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to load index page: {index_url}")
            return None, None, None

        soup = BeautifulSoup(response.text, "html.parser")
        doc_table = soup.find("table", class_="tableFile")
        if doc_table is None:
            print(f"⚠️ Could not find document table at: {index_url}")
            return None, None, None

        doc_link_tag = doc_table.find("a", href=lambda href: href and href.endswith(".htm") and not href.endswith("-index.htm"))
        if doc_link_tag is None:
            print(f"⚠️ No .htm filing document found: {index_url}")
            return None, None, None

        primary_doc = doc_link_tag['href'].lstrip("/")
        filing_url = f"https://www.sec.gov/{primary_doc}"

        filing_response = requests.get(filing_url, headers=headers, timeout=15)
        if filing_response.status_code == 200:
            return filing_url, filing_response.text, cik + "/" + accession_nodashes
        else:
            print(f"❌ Failed to download filing: {filing_url}")
            return filing_url, None, None

    except Exception as e:
        print(f"💥 Exception occurred: {e}")
        return None, None, None


def extract_and_store_filings(df, user_agent_email, s3_bucket, s3_prefix="raw_filings/", limit=None):
    """
    Loop through DataFrame, extract filing HTMLs, and upload to S3.
    Args:
        df (pd.DataFrame): Combined .idx metadata DataFrame
        user_agent_email (str): SEC-compliant User-Agent email
        s3_bucket (str): S3 bucket name
        s3_prefix (str): Folder prefix in S3
        limit (int): Max number of filings to extract (optional)
    """
    s3 = boto3.client("s3")
    count = 0

    for _, row in df.iterrows():
        if limit and count >= limit:
            break

        filing_url, html_content, s3_key_suffix = extract_filing_html_directly(row, user_agent_email)
        if html_content and s3_key_suffix:
            s3_key = f"{s3_prefix}{s3_key_suffix}.html"
            
            # Skip if already uploaded
            try:
                s3.head_object(Bucket=s3_bucket, Key=s3_key)
                print(f"🔁 Already exists in S3: {s3_key}")
                continue
            except s3.exceptions.ClientError:
                pass  # Not found, okay to proceed

            # Upload
            s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=html_content)
            print(f"✅ Uploaded to S3: s3://{s3_bucket}/{s3_key}")
            count += 1