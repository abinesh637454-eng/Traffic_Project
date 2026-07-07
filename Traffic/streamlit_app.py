import os

import pandas as pd
import plotly.express as px
import streamlit as st

from scripts.data_cleaning import CLEAN_CSV, RAW_CSV, clean_data, load_data, save_clean_csv

VALID_USERNAME = "admin"
VALID_PASSWORD = "traffic2026"


def load_clean_data():
    if not os.path.exists(CLEAN_CSV):
        df = load_data(RAW_CSV)
        cleaned = clean_data(df)
        save_clean_csv(cleaned, CLEAN_CSV)
    return pd.read_csv(CLEAN_CSV)


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "Login"
    if "login_error" not in st.session_state:
        st.session_state.login_error = ""


def authenticate(username: str, password: str) -> bool:
    return username == VALID_USERNAME and password == VALID_PASSWORD


def render_login_page():
    st.markdown("<div style='background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%); padding: 36px; border-radius: 18px;'>"
                "<h1 style='color:#fff; margin-bottom:10px;'>Traffic Peak Hour Portal</h1>"
                "<p style='color:#dbeafe; font-size:16px;'>Login to explore the traffic dataset, clean data, and visualize peak hours.</p>"
                "</div>", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        st.text_input("Username", key="username", help="Enter admin")
        st.text_input("Password", type="password", key="password", help="Enter traffic2026")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            if authenticate(st.session_state.username, st.session_state.password):
                st.session_state.logged_in = True
                st.session_state.page = "Dashboard"
                st.session_state.login_error = ""
                st.rerun()
            else:
                st.session_state.login_error = "Invalid username or password."

    if st.session_state.login_error:
        st.error(st.session_state.login_error)

    st.markdown("---")
    st.info("Use username: **admin** and password: **traffic2026** to access the dashboard.")


def render_sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Project Summary"], index=0 if st.session_state.page == "Dashboard" else 1)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.experimental_rerun()
    st.session_state.page = page


def render_dashboard_page():
    st.markdown("# Traffic Dashboard")
    st.markdown("Explore hourly volume, location impact, and vehicle class trends from cleaned traffic data.")

    if st.button("Refresh cleaned data"):
        raw_df = load_data(RAW_CSV)
        cleaned_df = clean_data(raw_df)
        save_clean_csv(cleaned_df, CLEAN_CSV)
        st.success("Cleaned data refreshed.")

    df = load_clean_data()
    st.sidebar.header("Filters")
    unique_dates = ["All"] + sorted(df["Date"].unique().tolist())
    unique_locations = ["All"] + sorted(df["Location"].unique().tolist())
    selected_date = st.sidebar.selectbox("Date", unique_dates, index=0)
    selected_location = st.sidebar.selectbox("Location", unique_locations, index=0)

    filtered = df.copy()
    if selected_date != "All":
        filtered = filtered[filtered["Date"] == selected_date]
    if selected_location != "All":
        filtered = filtered[filtered["Location"] == selected_location]

    total_records = len(filtered)
    total_vehicles = int(filtered["Vehicle Count"].sum())
    peak_hour = None
    if not filtered.empty:
        peak_hour = int(filtered.groupby("Hour")["Vehicle Count"].sum().idxmax())

    st.markdown("## Key Metrics")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Records", total_records, "cleaned")
    metric_col2.metric("Total Vehicles", total_vehicles, "aggregated")
    metric_col3.metric("Peak Hour", f"{peak_hour}:00" if peak_hour is not None else "N/A")

    st.markdown("---")
    st.markdown("### Traffic Filters")
    filter_col1, filter_col2 = st.columns(2)
    filter_col1.metric("Selected Date", selected_date)
    filter_col2.metric("Selected Location", selected_location)

    st.markdown("---")
    left, right = st.columns((2, 1))
    with left:
        if not filtered.empty:
            hourly = filtered.groupby("Hour")["Vehicle Count"].sum().reset_index()
            fig1 = px.bar(hourly, x="Hour", y="Vehicle Count", title="Hourly Traffic Volume", labels={"Hour": "Hour"}, template="plotly_white")
            st.plotly_chart(fig1, width="stretch")

            vehicle_type = filtered.groupby("Vehicle Type")["Vehicle Count"].sum().reset_index()
            fig3 = px.bar(vehicle_type, x="Vehicle Type", y="Vehicle Count", title="Vehicle Type Distribution", template="plotly_white")
            st.plotly_chart(fig3, width="stretch")
        else:
            st.warning("No entries match the selected filters.")

    with right:
        location = filtered.groupby("Location")["Vehicle Count"].sum().reset_index()
        fig2 = px.pie(location, names="Location", values="Vehicle Count", title="Traffic by Location", template="plotly_white")
        st.plotly_chart(fig2, width="stretch")

        st.markdown("### Quick Summary")
        st.write("- Clean dataset improves reliability.")
        st.write("- Use filters to narrow analysis by date and location.")
        st.write("- Peak hour is calculated from cleaned `Vehicle Count` totals.")

    st.markdown("---")
    with st.expander("View cleaned data table"):
        st.dataframe(filtered, width="stretch")


def render_summary_page():
    st.markdown("# Project Summary")
    st.markdown("A complete traffic analysis workflow that cleans incomplete records and surfaces peak hour insights.")

    st.markdown("## Objectives")
    st.write("- Clean incomplete and inconsistent traffic data")
    st.write("- Handle missing values and duplicate records")
    st.write("- Analyze traffic patterns and identify peak hours")
    st.write("- Create an interactive dashboard for insight delivery")

    st.markdown("## Dataset Fields")
    st.write("- Date")
    st.write("- Time")
    st.write("- Location")
    st.write("- Vehicle Count")
    st.write("- Vehicle Type")
    st.write("- Weather")
    st.write("- Road Condition")

    st.markdown("## Methodology")
    st.write("1. Load raw traffic data and clean date/time formats.")
    st.write("2. Remove duplicates and fill missing values.")
    st.write("3. Extract the hour for peak traffic analysis.")
    st.write("4. Aggregate vehicle counts by hour and location.")
    st.write("5. Visualize results and publish dashboard output.")

    st.markdown("## Tools Used")
    st.write("- Python")
    st.write("- Pandas")
    st.write("- Plotly")
    st.write("- Streamlit")
    st.write("- MongoDB (data storage, optional)")

    st.markdown("## Results")
    st.write("- Cleaned data reduces noise from missing and malformed entries.")
    st.write("- Peak hours usually appear in morning and evening windows.")
    st.write("- Easy dashboards help traffic management decisions.")

    st.markdown("## How to Use")
    st.write("1. Login to access the dashboard.")
    st.write("2. Use filters to explore date and location trends.")
    st.write("3. Review project summary for methodology and findings.")


def main():
    st.set_page_config(page_title="Traffic Peak Hour Analysis", layout="wide")
    init_session_state()

    if not st.session_state.logged_in:
        render_login_page()
        return

    render_sidebar()

    if st.session_state.page == "Dashboard":
        render_dashboard_page()
    elif st.session_state.page == "Project Summary":
        render_summary_page()


if __name__ == "__main__":
    main()
