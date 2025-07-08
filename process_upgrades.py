import pandas as pd
import logging
from common import DATA_FILE_UPGRADES, setup_logging

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
    df = load_and_map_upgrades()
    grouped_df = group_upgrades(df)
    logging.info(f"Grouped DataFrame shape: {grouped_df.shape}")

if __name__ == "__main__":
    main()
