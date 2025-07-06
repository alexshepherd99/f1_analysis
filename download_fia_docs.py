import os
import logging
import pandas as pd
import requests
from common import setup_logging, CACHE_FILE_FIA_DOCS, CACHE_FOLDER_FIA_DOCS


def load_and_update_fia_docs():
    setup_logging()
    # Try to load the cache file
    if os.path.exists(CACHE_FILE_FIA_DOCS):
        df = pd.read_csv(CACHE_FILE_FIA_DOCS)
        logging.info(f"Loaded FIA docs cache: {df.shape}")
    else:
        df = pd.DataFrame(columns=["season", "race_number", "pdf_url"])
        logging.info("No FIA docs cache found. Created empty dataframe: (0, 3)")

    # Get last entered values for defaults
    last_season = int(df["season"].iloc[-1]) if not df.empty else ""
    last_race_number = int(df["race number"].iloc[-1]) if not df.empty else 0

    while True:
        # Prompt for season
        default_season = f"[{last_season}]" if last_season else ""
        season_input = input(f"Enter season {default_season}: ").strip()
        season = int(season_input) if season_input else (last_season if last_season else int(input("Enter season: ")))
        
        # Prompt for race number
        next_race_number = last_race_number + 1 if last_race_number else 1
        default_race = f"[{next_race_number}]"
        race_input = input(f"Enter race number {default_race}: ").strip()
        race_number = int(race_input) if race_input else next_race_number

        # Prompt for PDF URL
        pdf_url = input("Enter PDF URL: ").strip()
        if not pdf_url:
            logging.error("PDF URL cannot be blank.")
            return

        # Validate PDF URL
        try:
            resp = requests.head(pdf_url, allow_redirects=True, timeout=10)
            if resp.status_code != 200 or not pdf_url.lower().endswith(".pdf"):
                raise Exception("Not a valid PDF URL or file does not exist.")
        except Exception as e:
            logging.error(f"PDF URL validation failed: {e}")
            return

        # Add new row
        df = pd.concat([df, pd.DataFrame([{
            "season": season,
            "race_number": race_number,
            "pdf_url": pdf_url
        }])], ignore_index=True)

        # Save cache
        df.to_csv(CACHE_FILE_FIA_DOCS, index=False)
        logging.info(f"Saved FIA docs cache: {df.shape}")

        # Ask to continue
        cont = input("Add another row? (y/N): ").strip().lower()
        if cont != "y":
            break
        last_season = season
        last_race_number = race_number


def download_missing_fia_pdfs():
    """
    Loads the FIA docs cache and downloads any missing PDFs to the local folder.
    """

    setup_logging()
    if not os.path.exists(CACHE_FILE_FIA_DOCS):
        logging.info("FIA docs cache file does not exist.")
        return

    if not os.path.exists(CACHE_FOLDER_FIA_DOCS):
        os.makedirs(CACHE_FOLDER_FIA_DOCS)
        logging.info(f"Created folder: {CACHE_FOLDER_FIA_DOCS}")

    df = pd.read_csv(CACHE_FILE_FIA_DOCS)
    logging.info(f"Loaded FIA docs cache: {df.shape}")

    for idx, row in df.iterrows():
        pdf_url = row["pdf_url"]
        filename = os.path.basename(pdf_url)
        local_path = os.path.join(CACHE_FOLDER_FIA_DOCS, filename)
        if os.path.exists(local_path):
            logging.info(f"Already downloaded: {filename}")
            continue
        try:
            logging.info(f"Downloading {pdf_url} ...")
            resp = requests.get(pdf_url, timeout=30)
            if resp.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(resp.content)
                logging.info(f"Downloaded and saved: {filename}")
            else:
                logging.info(f"Failed to download {pdf_url}: HTTP {resp.status_code}")
        except Exception as e:
            logging.info(f"Error downloading {pdf_url}: {e}")



if __name__ == "__main__":
    load_and_update_fia_docs()
    download_missing_fia_pdfs()
