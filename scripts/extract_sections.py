# scripts/extract_sections.py

import re
import pandas as pd
from datetime import datetime

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

def extract_sections_from_csv(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Applies section extraction to each row of Cleaned Text in the given CSV,
    and saves the output with new section columns.
    """
    df = pd.read_csv(input_csv)
    section_data = df["Cleaned Text"].apply(extract_10k_sections)

    df["Item 1 Text"] = section_data.apply(lambda x: x["Item 1"])
    df["Item 7 Text"] = section_data.apply(lambda x: x["Item 7"])
    df["Item 7A Text"] = section_data.apply(lambda x: x["Item 7A"])

    df.to_csv(output_csv, index=False)
    return df
