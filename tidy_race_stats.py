"""
This code was auto-generated with GitHub Copilot, with as minimal intervention as possible.  For this
file, I prompted each function one at a time until it worked as expected, then moved on a prompt for the
next function.  Smarter prompting could undoubtedly have got it to write more functionality in one go.
"""

import pandas as pd
import logging
from common import CACHE_FILE_DRIVER_STATS, setup_logging

# Configuration dictionary for team name mapping
TEAM_NAME_MAPPING = {
    "RB": "Racing Bulls",
    "AlphaTauri": "Racing Bulls",
    "Alfa Romeo": "Kick Sauber",
}


def add_driver_surname_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a new DataFrame with an added 'driver_surname' column,
    containing the last word from the 'driver_name' column.
    The input DataFrame is not modified.
    """
    df_copy = df.copy()
    df_copy["driver_surname"] = df_copy["driver_name"].str.split().str[-1]
    return df_copy


def add_team_name_mapped_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a new DataFrame with an added 'team_name_mapped' column,
    mapping values from 'team_name' using TEAM_NAME_MAPPING.
    If a team name is not in the mapping, the original value is used.
    The input DataFrame is not modified.
    """
    df_copy = df.copy()
    df_copy["team_name_mapped"] = df_copy["team_name"].map(TEAM_NAME_MAPPING).fillna(df_copy["team_name"])
    return df_copy


def main():
    setup_logging()
    logging.info(f"Loading dataframe from {CACHE_FILE_DRIVER_STATS}")
    df = pd.read_csv(CACHE_FILE_DRIVER_STATS)
    logging.info(f"Loaded dataframe shape: {df.shape}")

    df = add_driver_surname_column(df)
    logging.info(f"After add_driver_surname_column: {df.shape}")

    df = add_team_name_mapped_column(df)
    logging.info(f"After add_team_name_mapped_column: {df.shape}")

    df.to_csv(CACHE_FILE_DRIVER_STATS, index=False)
    logging.info(f"Saved dataframe to {CACHE_FILE_DRIVER_STATS} with shape: {df.shape}")


if __name__ == "__main__":
    main()
