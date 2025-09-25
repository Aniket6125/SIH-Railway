# pages/5_Dashboard.py
import os
import sys
import streamlit as st
import pandas as pd
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from utils.visualization import plot_gantt, plot_conflicts, fig_to_bytes
from utils.data_loader import load_csv

def main():
    st.set_page_config(page_title="Dashboard", layout="wide")

    # --- TITLE + LOGO SIDE BY SIDE ---
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("📊 5 - Dashboard")
    with col2:
        logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_container_width=True)
        else:
            st.warning("Logo not found at given path!")

    # Load timetable & conflicts
    timetable = st.session_state.get("timetable")
    if timetable is None:
        timetable = load_csv(None, os.path.join(ROOT, "sample_timetable_with_conflicts.csv"))
        st.session_state["timetable"] = timetable

    conflicts = st.session_state.get("detected_conflicts", [])
    audit = st.session_state.get("audit", [])

    # KPIs
    total_conflicts = len(conflicts)
    resolved = sum(1 for a in audit if a.get("action") in ("hold", "delay"))
    total_delay = 0
    for a in audit:
        if a.get("action") == "delay":
            total_delay += 7
        if a.get("action") == "hold":
            total_delay += 5

    st.subheader("Key Performance Indicators")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Conflicts Detected", total_conflicts)
    c2.metric("Conflicts Resolved", resolved)
    c3.metric("Total Delay (min)", total_delay)

    # Gantt chart (if enough data)
    st.subheader("Gantt Chart (simplified)")
    try:
        fig = plot_gantt(timetable)
        st.pyplot(fig)
        png = fig_to_bytes(fig)
        st.download_button("Download Gantt PNG", data=png, file_name="gantt.png", mime="image/png")
    except Exception as e:
        st.info("Gantt plotting not available for this dataset (expected columns: scheduled_departure, dwell_time).")
        st.write(str(e))

    # Conflicts breakdown
    st.subheader("Conflicts Breakdown")
    try:
        fig2 = plot_conflicts(conflicts)
        if fig2:
            st.pyplot(fig2)
    except Exception:
        st.info("No conflicts breakdown available.")

    # Recent audit
    st.subheader("Audit Trail (recent)")
    if audit:
        st.dataframe(pd.DataFrame(audit), use_container_width=True)
    else:
        st.write("No audit data yet.")

if __name__ == "__main__":
    main()
