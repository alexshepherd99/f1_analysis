import logging

CACHE_FILE_DRIVER_STATS = "data/f1_driver_stats.csv"
CACHE_FILE_DRIVER_PERF = "data/f1_driver_perf.csv"
CACHE_FILE_FIA_DOCS = "data/fia_docs.csv"
DATA_FILE_UPGRADES = "data/2025_fia_car_presentations.xlsx"
CACHE_FOLDER_FIA_DOCS = "fia_docs"


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
