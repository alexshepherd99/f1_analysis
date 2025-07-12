# f1_analysis

## Processing the FIA documents

I could not coerce Copilot to write code that would parse the PDF FIA car submission documents, even though they are a relatively simple tabular structure.  Rather than flog that one relentlessly, I got Gemini to process them for me, and write the outputs into a tabular format that can be appended to the bottom of "2025_fia_car_presentations.xlsx".  Of the various LLM coding tools I tried, Gemini had the most capacity to process files with the free tier.

### Gemini prompt to process FIA Car Presentation Summaries

Please can you analyse the attached files.  I would like you to create a single combined tabular structured output for all of them.  There will be a row in the table for each individual upgrade component.  Each row in the table will contain:
- the filename which this came from
- the team name
- all of the columns from the upgrades table in the file
Please do not include any rows in the output table when there were no upgrades for that team in that race.

# All documentation below here is auto-generated!

A toolkit for analyzing Formula 1 car upgrades, driver performance, and FIA documentation.

## Project Structure

- `common.py`: Defines shared constants (file paths, folder names) and a logging setup utility.
- `download_fia_docs.py`: CLI tool to add FIA car presentation PDF URLs to a cache and download missing PDFs to a local folder.
- `performance_rating.py`: Processes driver race stats, normalizes performance metrics, and outputs a performance rating CSV.
- `process_upgrades.py`: Loads, maps, and groups car upgrade data, merges it with FIA docs and driver performance, and outputs a combined Excel file.
- `query_race_stats.py`: Fetches race, driver, and lap data from the OpenF1 API, computes stats, and caches results.
- `tidy_race_stats.py`: Cleans and enriches the driver stats CSV with driver surnames and standardized team names.

## Data Files

- `data/f1_driver_stats.csv`: Cached driver stats (populated by `query_race_stats.py` and processed by others).
- `data/f1_driver_perf.csv`: Processed driver performance ratings (output of `performance_rating.py`).
- `data/fia_docs.csv`: FIA car presentation document metadata (managed by `download_fia_docs.py`).
- `data/2025_fia_car_presentations.xlsx`: Raw car upgrade data.
- `data/f1_driver_perf_upgrades.xlsx`: Final merged output of driver performance and upgrades.

## Usage

### 1. Download and Manage FIA Docs

Add new FIA car presentation PDFs and download missing files:

```sh
python download_fia_docs.py
```

### 2. Query Race Stats

Fetch and cache driver stats from OpenF1:

```sh
python query_race_stats.py
```

### 3. Tidy Race Stats

Standardize and enrich the driver stats CSV:

```sh
python tidy_race_stats.py
```

### 4. Rate Driver Performance

Normalize and score driver performance:

```sh
python performance_rating.py
```

### 5. Process Upgrades and Merge Data

Combine upgrades, FIA docs, and driver performance:

```sh
python process_upgrades.py
```

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies (e.g., `pandas`, `openpyxl`, `requests`).

## Script Details

### common.py

- Defines file paths, folder names, and a logging setup function used by all scripts.

### download_fia_docs.py

- Reads a list of FIA car presentation PDF URLs.
- Updates a cache of document metadata.
- Downloads missing PDFs to a local folder.

### query_race_stats.py

- Fetches race, driver, and lap data from the OpenF1 API.
- Computes and caches driver stats in CSV format.

### tidy_race_stats.py

- Cleans and enriches the driver stats CSV.
- Adds driver surnames and standardized team names.

### performance_rating.py

- Processes driver race stats.
- Normalizes performance metrics.
- Outputs a performance rating CSV.

### process_upgrades.py

- Loads and maps car upgrade data.
- Groups upgrades by team and event.
- Merges upgrades with FIA docs and driver performance.
- Outputs a combined Excel file for further analysis.

## Notes

- All scripts use logging for progress and error reporting.
- Data files are stored in the `data/` directory.
- FIA PDFs are downloaded to the `fia_docs/` folder.
- For details on each script, see the docstrings and comments in the respective files.
