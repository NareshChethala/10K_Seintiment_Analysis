# run_pipeline.py

from datetime import datetime
import os

from scripts.download_idx_files import download_idx_files_auto
from scripts.create_idx_dataframe import update_combined_dataframe
from scripts.download_multiple_10k import download_and_clean_10k_filings
from scripts.extract_sections import extract_sections_from_csv
from scripts.clean_section_data import clean_and_save_section_file

# Set paths
IDX_FOLDER = "data/idx"
RAW_DIR = "data/filings_raw"
WAREHOUSE_DIR = "data/warehouse"
USER_AGENT_EMAIL = "nareshchandra.chethala@gmail.com"
LIMIT_10K = 50  # Change as needed

def run_pipeline():
    os.makedirs(IDX_FOLDER, exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(WAREHOUSE_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # STEP 1: Download missing .idx files
    new_files = download_idx_files_auto(IDX_FOLDER, USER_AGENT_EMAIL)
    print(f"📥 Downloaded {new_files} new .idx files (if any).")

    # STEP 2: Combine .idx files into a DataFrame
    combined_df = update_combined_dataframe(IDX_FOLDER, os.path.join(WAREHOUSE_DIR, "combined_data.csv"))
    print(f"📂 Combined index contains {len(combined_df)} filings.")

    # STEP 3: Download and clean raw 10-K filings
    raw_csv = download_and_clean_10k_filings(
        df=combined_df,
        user_agent_email=USER_AGENT_EMAIL,
        output_dir=RAW_DIR,
        limit=LIMIT_10K
    )
    print(f"🧾 Raw filings saved to: {raw_csv}")

    # STEP 4: Extract sections (Item 1, 7, 7A)
    sectioned_csv = os.path.join(WAREHOUSE_DIR, f"filings_with_sections_{timestamp}.csv")
    df_with_sections = extract_sections_from_csv(raw_csv, sectioned_csv)
    print(f"📑 Sections saved to: {sectioned_csv}")

    # STEP 5: Final cleaning
    cleaned_csv = os.path.join(WAREHOUSE_DIR, f"cleaned_final_{timestamp}.csv")
    cleaned_df = clean_and_save_section_file(sectioned_csv, cleaned_csv)
    print(f"✅ Cleaned data saved to: {cleaned_csv} ({len(cleaned_df)} rows)")

if __name__ == "__main__":
    run_pipeline()
