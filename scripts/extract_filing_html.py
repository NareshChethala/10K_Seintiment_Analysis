# extract_filing_html.py

import requests
import pandas as pd
from bs4 import BeautifulSoup

def extract_filing_html_directly(row, user_agent_email):
    """
    Extracts the actual 10-K filing HTML content from a row in the .idx-derived dataframe
    by locating the full-text .htm file from the SEC index page.

    Args:
        row (pd.Series): A row from the DataFrame with 'Filename' column.
        user_agent_email (str): Email address to set as User-Agent (per SEC requirement).

    Returns:
        tuple: (filing_url, html_content) or (None, None) if any error occurs.
    """
    try:
        filename = row['Filename'].strip().replace(" ", "")
        path_parts = filename.split("/")

        if len(path_parts) < 4:
            print(f"Invalid path in Filename: {filename}")
            return None, None

        cik = path_parts[2]
        accession_with_dashes = path_parts[3]
        accession_nodashes = accession_with_dashes.replace("-", "")
        index_filename = accession_with_dashes + "-index.htm"

        index_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodashes}/{index_filename}"
        headers = {"User-Agent": user_agent_email}

        response = requests.get(index_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to load index page: {index_url}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        doc_table = soup.find("table", class_="tableFile")
        if doc_table is None:
            print(f"⚠️ Could not find document table at: {index_url}")
            return None, None

        doc_link_tag = doc_table.find("a", href=lambda href: href and href.endswith(".htm") and not href.endswith("-index.htm"))
        if doc_link_tag is None:
            print(f"⚠️ No .htm filing document found in index page: {index_url}")
            return None, None

        primary_doc = doc_link_tag['href'].lstrip("/")  # remove leading slash
        filing_url = f"https://www.sec.gov/{primary_doc}"  # FIXED — no double /Archives

        filing_response = requests.get(filing_url, headers=headers, timeout=15)
        if filing_response.status_code == 200:
            print(f"✅ Downloaded: {filing_url}")
            return filing_url, filing_response.text
        else:
            print(f"❌ Failed to download filing from: {filing_url}")
            return filing_url, None

    except Exception as e:
        print(f"💥 Exception occurred: {e}")
        return None, None
