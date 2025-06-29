import logging

CACHE_FILE_DRIVER_STATS = "data/f1_driver_stats.csv"


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
