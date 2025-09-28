# scripts/extract_sections.py

import re
import boto3

def extract_10k_sections(text):
    """
    Extracts Item 1, 7, and 7A from cleaned filing text using regex patterns.
    """
    if not isinstance(text, str) or len(text) < 100:
        return {"Item 1": "", "Item 7": "", "Item 7A": ""}

    text_lower = text.lower()

    patterns = {
        "Item 1": r"(item[\s]*1[\s\.:\-–—]*((business)?[^a-z0-9]{0,10}))",
        "Item 7": r"(item[\s]*7[^a-z0-9]{0,10}(management'?s)?[^a-z0-9]{0,10}(discussion)?)",
        "Item 7A": r"(item[\s]*7a[^a-z0-9]{0,10}(quantitative)?[^a-z0-9]{0,10}(market)?[^a-z0-9]{0,10}(risk)?)"
    }

    matches = []
    for section, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            matches.append((section, match.start()))

    matches.sort(key=lambda x: x[1])
    sections = {}
    for i in range(len(matches)):
        name, start = matches[i]
        end = matches[i+1][1] if i + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()

    return {
        "Item 1": sections.get("Item 1", ""),
        "Item 7": sections.get("Item 7", ""),
        "Item 7A": sections.get("Item 7A", "")
    }


def extract_sections_and_upload(bucket, cleaned_prefix="cleaned_filings/", output_prefix="sectioned_filings/", limit=None):
    """
    Processes cleaned filings from S3, extracts sections, and uploads each section to S3.
    """
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=cleaned_prefix)

    processed = 0

    for page in page_iterator:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if not key.endswith(".txt"):
                continue

            base_name = key.split("/")[-1].replace(".txt", "")
            try:
                # Read cleaned text
                response = s3.get_object(Bucket=bucket, Key=key)
                cleaned_text = response["Body"].read().decode("utf-8")

                # Extract sections
                sections = extract_10k_sections(cleaned_text)

                if not any(sections.values()):
                    print(f"⚠️ No sections extracted from {key}")
                    continue

                # Upload each section
                for section_name, section_text in sections.items():
                    if not section_text.strip():
                        continue
                    section_key = f"{output_prefix}{base_name}/{section_name.replace(' ', '_')}.txt"
                    s3.put_object(Bucket=bucket, Key=section_key, Body=section_text)
                    print(f"✅ Uploaded section: s3://{bucket}/{section_key}")

                processed += 1
                if limit and processed >= limit:
                    return
            except Exception as e:
                print(f"❌ Error processing {key}: {e}")