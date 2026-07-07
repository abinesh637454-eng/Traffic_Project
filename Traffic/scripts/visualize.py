import os
import pandas as pd
import matplotlib.pyplot as plt

CLEAN_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "clean_traffic_data.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "plots")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def plot_hourly(df: pd.DataFrame):
    grouped = df.groupby("Hour")["Vehicle Count"].sum().reindex(range(0, 24), fill_value=0)
    plt.figure(figsize=(12, 6))
    grouped.plot(kind="bar", color="#2563eb")
    plt.title("Total Vehicle Count by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Vehicle Count")
    plt.tight_layout()
    file_path = os.path.join(OUTPUT_DIR, "hourly_vehicle_count.png")
    plt.savefig(file_path)
    plt.close()
    print(f"Saved hourly chart to {file_path}")


def plot_location(df: pd.DataFrame):
    grouped = df.groupby("Location")["Vehicle Count"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    grouped.plot(kind="bar", color="#0f766e")
    plt.title("Vehicle Count by Location")
    plt.xlabel("Location")
    plt.ylabel("Vehicle Count")
    plt.tight_layout()
    file_path = os.path.join(OUTPUT_DIR, "location_vehicle_count.png")
    plt.savefig(file_path)
    plt.close()
    print(f"Saved location chart to {file_path}")


def main():
    ensure_output_dir()
    df = load_data(CLEAN_CSV)
    plot_hourly(df)
    plot_location(df)


if __name__ == "__main__":
    main()
