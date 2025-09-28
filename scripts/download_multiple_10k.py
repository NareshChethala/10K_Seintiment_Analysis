# scripts/download_multiple_10k.py

import os
import pandas as pd
from datetime import datetime
from scripts.extract_filing_html import extract_filing_html_directly
from scripts.clean_filing_html import clean_filing_html

def download_and_clean_10k_filings(
    df: pd.DataFrame,
    user_agent_email: str,
    output_dir: str,
    limit: int = 100
) -> str:
    """
    Downloads, extracts, and cleans 10-K filings.

    Args:
        df (pd.DataFrame): Combined index DataFrame
        user_agent_email (str): SEC-required user agent
        output_dir (str): Directory to save raw output CSV
        limit (int): Number of 10-K filings to process

    Returns:
        str: Path to saved CSV file
    """
    os.makedirs(output_dir, exist_ok=True)
    df_10k = df[df['Form Type'].str.upper() == '10-K'].reset_index(drop=True)

    results = []
    for _, row in df_10k.head(limit).iterrows():
        url, html_text = extract_filing_html_directly(row, user_agent_email)
        if html_text:
            cleaned_text = clean_filing_html(html_text)
            results.append({
                "Company Name": row['Company Name'],
                "CIK": row['CIK'],
                "Date Filed": row['Date Filed'],
                "Filing URL": url,
                "Filing Text": html_text,
                "Cleaned Text": cleaned_text
            })

    output_df = pd.DataFrame(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    out_file = os.path.join(output_dir, f"raw_10k_filings_{timestamp}.csv")
    output_df.to_csv(out_file, index=False)

    return out_file
