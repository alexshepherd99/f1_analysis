"""
This file is the only one that had most of the constants written by me, and just the helper function
prompted to Copilot.  As with the other scripts, I'm sure that smarter prompting could have overcome
this, so that it generated consistently labelled constants for me.
"""

import logging

CACHE_FILE_DRIVER_STATS = "data/f1_driver_stats.csv"
CACHE_FILE_DRIVER_PERF = "data/f1_driver_perf.csv"
CACHE_FILE_FIA_DOCS = "data/fia_docs.csv"
DATA_FILE_UPGRADES = "data/2025_fia_car_presentations.xlsx"
OUTPUT_FILE_PERF_AND_UPGRADES = "data/f1_driver_perf_upgrades.xlsx"
CACHE_FOLDER_FIA_DOCS = "fia_docs"


def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
