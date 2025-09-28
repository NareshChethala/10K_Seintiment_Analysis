# scripts/clean_section_data.py

import pandas as pd
from datetime import datetime

def clean_section_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops rows with null or empty text in key sections and very short filings.
    """
    df = df.dropna(subset=["Item 1 Text", "Item 7 Text", "Item 7A Text", "Cleaned Text"])

    df = df[
        (df["Item 1 Text"].str.strip() != "") &
        (df["Item 7 Text"].str.strip() != "") &
        (df["Item 7A Text"].str.strip() != "") &
        (df["Cleaned Text"].str.strip() != "")
    ]

    df = df[df["Cleaned Text"].str.len() >= 500]
    df = df.reset_index(drop=True)
    return df

def clean_and_save_section_file(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Loads the extracted-sections CSV, cleans it, and saves to a new cleaned CSV.

    Args:
        input_csv (str): Path to section-extracted CSV
        output_csv (str): Path to cleaned final output

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    df = pd.read_csv(input_csv)
    cleaned_df = clean_section_dataframe(df)
    cleaned_df.to_csv(output_csv, index=False)
    return cleaned_df
