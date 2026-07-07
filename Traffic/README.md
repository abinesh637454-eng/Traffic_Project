# Traffic Data Cleaning & Peak Hour Analysis

This project demonstrates a complete traffic analysis workflow using Python, Pandas, Matplotlib, Django, and MongoDB.

## Project Goals
- Clean incomplete and inconsistent traffic data
- Handle missing values and duplicate records
- Fix incorrect date/time formats
- Extract features for peak hour analysis
- Visualize traffic patterns with charts
- Build a Django dashboard for interactive filtering
- Store cleaned data in MongoDB for fast retrieval

## Structure
- `data/`: sample raw and cleaned traffic CSV data
- `scripts/`: data cleaning and visualization scripts
- `traffic_dashboard/`: Django dashboard application
- `powerbi/`: guidance for Power BI dashboard creation

## Setup
1. Create a Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the cleaning script:
   ```powershell
   python scripts\data_cleaning.py
   ```
4. Start MongoDB locally and then ingest cleaned data:
   ```powershell
   python scripts\data_cleaning.py --save-mongo
   ```
5. Run Django migrations and start the dashboard:
   ```powershell
   cd traffic_dashboard
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Notes
- The project includes a sample dataset at `data/traffic_data.csv`.
- Cleaned output is saved to `data/clean_traffic_data.csv`.
- The Django dashboard reads aggregated traffic metrics from MongoDB.
- Power BI guidance is added to `powerbi/README.md`.
