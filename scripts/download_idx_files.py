# scripts/download_idx_files.py

import os
import time
import requests
from datetime import datetime

BASE_URL = 'https://www.sec.gov/Archives/edgar/full-index/'

def download_file(url: str, path: str, headers: dict):
    """Download file with retry and headers."""
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def get_quarters_for_year(year: int, current_year: int, current_qtr: int):
    """Returns valid quarters for a given year, capped to current quarter if this year."""
    all_quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
    if year == current_year:
        return all_quarters[:current_qtr]
    return all_quarters

def download_idx_files_auto(save_dir: str, user_agent_email: str) -> int:
    """
    Automatically downloads missing .idx files from 1993 to current year & quarter.

    Args:
        save_dir (str): Directory to store .idx files.
        user_agent_email (str): Email to comply with SEC user-agent policy.

    Returns:
        int: Number of new files downloaded.
    """
    os.makedirs(save_dir, exist_ok=True)
    headers = {"User-Agent": user_agent_email}
    new_files = 0

    now = datetime.now()
    current_year = now.year
    current_qtr = (now.month - 1) // 3 + 1

    for year in range(1993, current_year + 1):
        quarters = get_quarters_for_year(year, current_year, current_qtr)
        for qtr in quarters:
            filename = f"{year}_{qtr}_company.idx"
            path = os.path.join(save_dir, filename)
            url = f"{BASE_URL}{year}/{qtr}/company.idx"

            if not os.path.exists(path):
                try:
                    download_file(url, path, headers)
                    time.sleep(1)  # Be polite to SEC servers
                    new_files += 1
                except Exception:
                    continue

    return new_files
