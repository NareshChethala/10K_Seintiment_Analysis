# scripts/create_idx_dataframe.py

import os
import pandas as pd

def load_data_from_directory(source_dir: str) -> pd.DataFrame:
    """
    Loads all .idx files in directory and returns combined DataFrame.

    Args:
        source_dir (str): Path to directory containing .idx files.

    Returns:
        pd.DataFrame: Combined data from all .idx files.
    """
    colspecs = [(0, 62), (62, 74), (74, 86), (86, 98), (98, None)]
    column_names = ['Company Name', 'Form Type', 'CIK', 'Date Filed', 'Filename']
    dataframe_collection = []

    for file_name in os.listdir(source_dir):
        if file_name.endswith('.idx'):
            file_path = os.path.join(source_dir, file_name)
            try:
                df = pd.read_fwf(file_path, colspecs=colspecs, skiprows=9, names=column_names)
                dataframe_collection.append(df)
            except Exception:
                continue

    if not dataframe_collection:
        return pd.DataFrame()

    combined_df = pd.concat(dataframe_collection, ignore_index=True)
    combined_df.columns = combined_df.columns.str.strip()
    for col in combined_df.columns:
        if combined_df[col].dtype == "object":
            combined_df[col] = combined_df[col].str.strip()

    return combined_df

def update_combined_dataframe(idx_folder: str, output_csv_path: str) -> pd.DataFrame:
    """
    Updates or creates combined .idx metadata CSV.

    Args:
        idx_folder (str): Directory containing .idx files
        output_csv_path (str): Output path for combined CSV

    Returns:
        pd.DataFrame: Full combined DataFrame
    """
    new_df = load_data_from_directory(idx_folder)

    if os.path.exists(output_csv_path):
        existing_df = pd.read_csv(output_csv_path)
        combined_df = pd.concat([existing_df, new_df])
        combined_df.drop_duplicates(subset="Filename", inplace=True)
        combined_df.reset_index(drop=True, inplace=True)
    else:
        combined_df = new_df

    combined_df.to_csv(output_csv_path, index=False)
    return combined_df
