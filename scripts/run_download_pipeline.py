# run_download_pipeline.py

import pandas as pd
from download_multiple_10k import download_multiple_10k_filings

def main():
    csv_path = input("Enter path to your combined .idx CSV file (e.g., combined_data.csv): ").strip()
    user_agent = input("Enter your email (User-Agent for SEC scraping): ").strip()
    output_csv = input("Enter output filename (e.g., filings_output.csv): ").strip()

    try:
        df = pd.read_csv(csv_path)
        print("✅ Index CSV loaded.")
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return

    # Filter only 10-Ks
    filtered = df[df["Form Type"].str.upper() == "10-K"].reset_index(drop=True)

    # Download and clean filings
    filings_df = download_multiple_10k_filings(filtered, user_agent)

    if filings_df.empty:
        print("⚠️ No filings downloaded.")
        return

    # Save results silently
    try:
        filings_df.to_csv(output_csv, index=False)
        print(f"📁 Saved cleaned filings to {output_csv}")
    except Exception as e:
        print(f"❌ Failed to save output CSV: {e}")

if __name__ == "__main__":
    main()
