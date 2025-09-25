# pages/6_Comprehensive_Reporting.py
import os
import sys
import streamlit as st
import pandas as pd
import json
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from utils.reporting import generate_conflict_report
from utils.data_loader import load_csv

def main():
    st.set_page_config(page_title="Comprehensive Reporting", layout="wide")

    # --- TITLE + LOGO SIDE BY SIDE ---
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("📑 6 - Comprehensive Reporting")
    with col2:
        logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_container_width=True)
        else:
            st.warning("Logo not found at given path!")

    timetable = st.session_state.get("timetable")
    if timetable is None:
        timetable = load_csv(None, os.path.join(ROOT, "sample_timetable_with_conflicts.csv"))
        st.session_state["timetable"] = timetable

    conflicts = st.session_state.get("detected_conflicts", [])
    audit = st.session_state.get("audit", [])

    st.subheader("Timetable Snapshot")
    st.dataframe(timetable, use_container_width=True)

    st.subheader("Detected Conflicts")
    st.write(conflicts)

    st.subheader("Audit Trail")
    st.write(audit)

    # Export options
    st.markdown("### Export reports")
    if st.button("Export Conflicts CSV"):
        rpt = generate_conflict_report(conflicts)
        st.download_button(
            "Download Conflicts CSV",
            data=rpt.to_csv(index=False),
            file_name="conflicts_report.csv",
            mime="text/csv"
        )

    if st.button("Export Timetable (CSV)"):
        st.download_button(
            "Download Timetable CSV",
            data=timetable.to_csv(index=False),
            file_name="timetable.csv",
            mime="text/csv"
        )

    if st.button("Export Audit (JSON)"):
        st.download_button(
            "Download Audit JSON",
            data=json.dumps(audit, default=str),
            file_name="audit.json",
            mime="application/json"
        )

    # Combined report (JSON)
    if st.button("Export Combined Report (JSON)"):
        combined = {
            "timetable": json.loads(timetable.to_json(orient="records")),
            "conflicts": conflicts,
            "audit": audit
        }
        st.download_button(
            "Download Combined JSON",
            data=json.dumps(combined, default=str),
            file_name="combined_report.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
