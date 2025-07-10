import os
import pandas as pd
import logging
from common import DATA_FILE_UPGRADES, CACHE_FILE_FIA_DOCS, setup_logging

TEAM_NAME_MAPPING = {
    "Aston Martin Aramco F1 Team": "Aston Martin",
    "ATLASSIAN WILLIAMS RACING": "Williams",
    "BWT Alpine F1 Team": "Alpine",
    "McLaren Formula 1 Team": "McLaren",
    "Mercedes-AMG PETRONAS F1 Team": "Mercedes",
    "MONEYGRAM HAAS F1 TEAM": "Haas F1 Team",
    "SCUDERIA FERRARI HP": "Ferrari",
    "Stake F1 Team KICK Sauber": "Kick Sauber",
    "Visa Cash App Racing Bulls": "Racing Bulls"
}

def load_fia_docs_with_filename():
    """
    Loads the FIA docs dataframe from CACHE_FILE_FIA_DOCS (CSV), adds a 'Filename' column
    extracted from the 'pdf_url' column, logs progress, and returns the new dataframe.
    """
    logging.info(f"Loading FIA docs from {CACHE_FILE_FIA_DOCS}")
    df = pd.read_csv(CACHE_FILE_FIA_DOCS)
    logging.info(f"Loaded DataFrame shape: {df.shape}")
    if "pdf_url" in df.columns:
        logging.info("Adding 'Filename' column based on 'pdf_url'")
        df["Filename"] = df["pdf_url"].apply(lambda url: os.path.basename(url) if pd.notnull(url) else None)
    else:
        logging.warning("'pdf_url' column not found in DataFrame; 'Filename' column not added.")
    logging.info(f"DataFrame shape after adding 'Filename': {df.shape}")
    return df

def load_and_map_upgrades():
    df = pd.read_excel(DATA_FILE_UPGRADES)
    df["team_name_mapped"] = df["Team Name"].map(TEAM_NAME_MAPPING).fillna(df["Team Name"])
    logging.info(f"Loaded file: {DATA_FILE_UPGRADES}")
    logging.info(f"DataFrame shape: {df.shape}")
    return df

def group_upgrades(df):
    grouped = df.groupby(["Filename", "team_name_mapped"]).agg(
        upgrade_count=("Filename", "size"),
        circuit_specific_any=("Primary reason for update", lambda x: x.str.contains("circuit specific", case=False, na=False).any())
    ).reset_index()
    return grouped

def main():
    setup_logging()
    df_upgrades = load_and_map_upgrades()
    df_upgrades = group_upgrades(df_upgrades)
    logging.info(f"Grouped DataFrame shape: {df_upgrades.shape}")

    df_fia_docs = load_fia_docs_with_filename()

    df_merged = pd.merge(df_upgrades, df_fia_docs, on="Filename", how="left")
    if len(df_merged) != len(df_upgrades):
        raise Exception(f"Row count changed after merge: {len(df_upgrades)} -> {len(df_merged)}")
    logging.info(f"Merged DataFrame shape: {df_merged.shape}")

if __name__ == "__main__":
    main()
