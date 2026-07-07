import argparse
import os
from datetime import datetime

import numpy as np
import pandas as pd
from pymongo import MongoClient

RAW_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "traffic_data.csv")
CLEAN_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "clean_traffic_data.csv")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "traffic_analysis"
COLLECTION_NAME = "cleaned_traffic"


def load_data(source_path: str) -> pd.DataFrame:
    df = pd.read_csv(source_path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Fix date and time formats
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce").dt.time

    # Remove rows that cannot be parsed for date or time
    df = df[~df["Date"].isna()]
    df = df[~df["Time"].isna()]

    # Standardize string fields and fill missing values
    df["Location"] = df["Location"].fillna("Unknown").astype(str).str.strip()
    df["Vehicle Type"] = df["Vehicle Type"].fillna("Unknown").astype(str).str.strip()
    df["Weather"] = df["Weather"].fillna("Unknown").astype(str).str.strip()
    df["Road Condition"] = df["Road Condition"].fillna("Unknown").astype(str).str.strip()

    df["Vehicle Count"] = pd.to_numeric(df["Vehicle Count"], errors="coerce").fillna(0).astype(int)

    # Normalize field formatting
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["Time"] = df["Time"].apply(lambda value: value.strftime("%H:%M") if pd.notna(value) else "00:00")
    df["Hour"] = df["Time"].str.slice(0, 2).astype(int)

    # Remove exact duplicate rows
    df = df.drop_duplicates(subset=["Date", "Time", "Location", "Vehicle Count", "Vehicle Type"])
    df = df.reset_index(drop=True)

    return df


def save_clean_csv(df: pd.DataFrame, destination_path: str) -> None:
    df.to_csv(destination_path, index=False)
    print(f"Cleaned data saved to {destination_path}")


def save_to_mongo(df: pd.DataFrame, mongo_uri: str, db_name: str, collection_name: str) -> None:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    collection.delete_many({})
    records = df.to_dict(orient="records")
    collection.insert_many(records)
    client.close()
    print(f"Cleaned data saved to MongoDB database '{db_name}', collection '{collection_name}'")


def aggregate_hourly(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("Hour", as_index=False)["Vehicle Count"].sum().sort_values("Hour")
    return grouped


def print_summary(df: pd.DataFrame, original_count: int) -> None:
    print("Data cleaning summary")
    print("---------------------")
    print(f"Original record count: {original_count}")
    print(f"Cleaned record count : {len(df)}")
    print(df["Hour"].value_counts().sort_index())


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean traffic dataset and optionally store it in MongoDB.")
    parser.add_argument("--save-mongo", action="store_true", help="Save cleaned data to MongoDB")
    args = parser.parse_args()

    df = load_data(RAW_CSV)
    original_count = len(df)
    cleaned_df = clean_data(df)
    save_clean_csv(cleaned_df, CLEAN_CSV)
    print_summary(cleaned_df, original_count)

    if args.save_mongo:
        save_to_mongo(cleaned_df, MONGO_URI, DB_NAME, COLLECTION_NAME)


if __name__ == "__main__":
    main()
