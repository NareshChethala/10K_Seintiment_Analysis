import os
import pandas as pd
import boto3
import io

colspecs = [(0, 62), (62, 74), (74, 86), (86, 98), (98, None)]
column_names = ['Company Name', 'Form Type', 'CIK', 'Date Filed', 'Filename']


def parse_idx_file_from_string(content: str) -> pd.DataFrame:
    df = pd.read_fwf(io.StringIO(content), colspecs=colspecs, skiprows=9, names=column_names)
    df.columns = df.columns.str.strip()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    return df


def load_data_from_local_directory(source_dir: str) -> pd.DataFrame:
    dataframes = []
    for file_name in os.listdir(source_dir):
        if file_name.endswith(".idx"):
            file_path = os.path.join(source_dir, file_name)
            try:
                df = pd.read_fwf(file_path, colspecs=colspecs, skiprows=9, names=column_names)
                df.columns = df.columns.str.strip()
                for col in df.columns:
                    if df[col].dtype == "object":
                        df[col] = df[col].str.strip()
                dataframes.append(df)
            except Exception:
                continue
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()


def load_data_from_s3(bucket: str, prefix="idx/") -> pd.DataFrame:
    s3 = boto3.client("s3")
    result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    all_dfs = []

    for obj in result.get("Contents", []):
        key = obj["Key"]
        if not key.endswith(".idx"):
            continue
        file_obj = s3.get_object(Bucket=bucket, Key=key)
        content = file_obj["Body"].read().decode("latin-1")
        df = parse_idx_file_from_string(content)
        if not df.empty:
            df["source_file"] = key
            all_dfs.append(df)

    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()


def update_combined_dataframe(idx_source_dir: str, output_csv_path: str, s3_bucket: str = None, upload_key: str = None, use_s3: bool = False) -> pd.DataFrame:
    """
    Combines .idx metadata from local or S3 into one DataFrame.

    Args:
        idx_source_dir (str): Local folder with .idx files
        output_csv_path (str): Local CSV file to store combined metadata
        s3_bucket (str): Optional bucket to upload final CSV
        upload_key (str): Optional S3 key (e.g., 'processed/combined_idx.csv')
        use_s3 (bool): Whether to read .idx files from S3 or not

    Returns:
        pd.DataFrame: Combined DataFrame
    """
    if use_s3 and s3_bucket:
        new_df = load_data_from_s3(bucket=s3_bucket)
    else:
        new_df = load_data_from_local_directory(idx_source_dir)

    if os.path.exists(output_csv_path):
        existing_df = pd.read_csv(output_csv_path)
        combined_df = pd.concat([existing_df, new_df])
        combined_df.drop_duplicates(subset="Filename", inplace=True)
        combined_df.reset_index(drop=True, inplace=True)
    else:
        combined_df = new_df

    # Save locally
    combined_df.to_csv(output_csv_path, index=False)

    # Upload to S3
    if s3_bucket and upload_key:
        s3 = boto3.client("s3")
        buffer = io.StringIO()
        combined_df.to_csv(buffer, index=False)
        s3.put_object(Bucket=s3_bucket, Key=upload_key, Body=buffer.getvalue())

    return combined_df