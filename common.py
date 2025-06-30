import logging

CACHE_FILE_DRIVER_STATS = "data/f1_driver_stats.csv"
CACHE_FILE_DRIVER_PERF = "data/f1_driver_perf.csv"


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
