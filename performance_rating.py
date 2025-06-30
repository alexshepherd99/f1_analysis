import pandas as pd
import logging

from common import setup_logging, CACHE_FILE_DRIVER_STATS, CACHE_FILE_DRIVER_PERF


def filter_by_session_key(df: pd.DataFrame, session_key) -> pd.DataFrame:
    """
    Returns a new DataFrame filtered to only rows with the given session_key.
    """
    return df[df['session_key'] == session_key].copy()


def get_normalized_position(
    df: pd.DataFrame,
    session_key,
    driver_number,
    column_name: str,
    higher_is_better: bool
) -> float:
    """
    Returns a float between 0 and 1 indicating the normalized position of the specified row's value
    within all values for the given session_key in the specified column.
    If higher_is_better is True, 1 means best (highest value), 0 means worst (lowest value).
    If higher_is_better is False, 0 means best (lowest value), 1 means worst (highest value).
    """
    # Filter for the specific row
    row = df[(df['session_key'] == session_key) & (df['driver_number'] == driver_number)]
    if len(row) != 1:
        raise ValueError(f"Expected exactly one row for session_key={session_key}, driver_number={driver_number}, found {len(row)}")
    row_value = row.iloc[0][column_name]

    # Get all rows for the session
    df_session = filter_by_session_key(df, session_key)
    col_values = df_session[column_name]

    min_val = col_values.min()
    max_val = col_values.max()

    if max_val == min_val:
        # Avoid division by zero; all values are the same
        return 1.0 if higher_is_better else 0.0

    if higher_is_better:
        normalized = (row_value - min_val) / (max_val - min_val)
    else:
        normalized = (max_val - row_value) / (max_val - min_val)

    return normalized


def add_normalized_score_column(
    df: pd.DataFrame,
    column_name: str,
    higher_is_better: bool
) -> pd.DataFrame:
    """
    Returns a new DataFrame with an added column containing normalized scores for the specified column.
    The new column is named 'score_{column_name}'.
    The original DataFrame is not modified.
    """
    df_copy = df.copy()
    score_col = f"score_{column_name}"

    def calc_score(row):
        return get_normalized_position(
            df,
            row['session_key'],
            row['driver_number'],
            column_name,
            higher_is_better
        )

    df_copy[score_col] = df_copy.apply(calc_score, axis=1)
    return df_copy


def main():
    df_driver_stats = pd.read_csv(CACHE_FILE_DRIVER_STATS)
    logging.info(f"Loaded driver stats: {df_driver_stats.shape}")

    df_driver_stats = add_normalized_score_column(df_driver_stats, "best_lap_time", higher_is_better=False)
    logging.info(f"After best_lap_time normalization: {df_driver_stats.shape}")

    df_driver_stats = add_normalized_score_column(df_driver_stats, "avg_lap_time", higher_is_better=False)
    logging.info(f"After avg_lap_time normalization: {df_driver_stats.shape}")

    df_driver_stats = add_normalized_score_column(df_driver_stats, "position_change", higher_is_better=True)
    logging.info(f"After position_change normalization: {df_driver_stats.shape}")

    df_driver_stats = add_normalized_score_column(df_driver_stats, "final_position", higher_is_better=False)
    logging.info(f"After final_position normalization: {df_driver_stats.shape}")

    df_driver_stats.to_csv(CACHE_FILE_DRIVER_PERF, index=False)
    logging.info(f"Saved processed driver stats to {CACHE_FILE_DRIVER_PERF}")


if __name__ == "__main__":
    setup_logging()
    main()
