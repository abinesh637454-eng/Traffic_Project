# Power BI Dashboard Guidance

This folder contains recommendations for building an advanced Power BI dashboard from cleaned traffic data.

## Recommended Visuals
- Line chart: Total vehicle count by hour
- Clustered bar chart: Traffic count by location
- Donut or pie chart: Vehicle type distribution
- Slicer filters: Date and location
- KPI cards: Peak hour vehicle count, highest-traffic location, busiest vehicle type

## Data Source
1. Use `data/clean_traffic_data.csv` as a data source.
2. Load the cleaned traffic dataset into Power BI Desktop.
3. Create relationships or calculated columns if needed.

## Suggested Data Model
- `Date`: use as a date type
- `Hour`: use as a numeric or categorical field
- `Vehicle Count`: aggregate by sum
- `Location`, `Vehicle Type`, `Weather`, `Road Condition`: use for slicing and filtering

## Peak Hour Highlight
- Create a measure using `MAXX` or `TOPN` to find the hour with the highest total vehicle count.
- Add a card visualization to highlight the peak hour.

## Notes
- Power BI Desktop can connect directly to MongoDB if you use a premium custom connector, but this sample uses the cleaned CSV for simplicity.
- Add a refresh schedule if you export cleaned data from MongoDB into a refreshable data source.
