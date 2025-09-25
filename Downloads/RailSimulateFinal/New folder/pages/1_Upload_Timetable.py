import os
import sys
import streamlit as st
import pandas as pd
from PIL import Image

# --- ensure project root in path ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from utils.data_loader import load_csv

def main():
    st.set_page_config(page_title="Upload Timetable", layout="wide")

    # --- TITLE + LOGO SIDE BY SIDE ---
    col1, col2 = st.columns([8, 2])  # adjust ratio if needed
    with col1:
        st.title("📂 1 - Upload Timetable")
    with col2:
        logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_container_width=True)
        else:
            st.warning("Logo not found at given path!")

    st.markdown("""
    Upload your timetable in **CSV format**.  
    The system will load it into memory and make it available to all subsequent pages.
    """)

    uploaded = st.file_uploader("Upload timetable CSV", type=["csv"])

    if uploaded is not None:
        df = load_csv(uploaded)
        st.session_state["timetable"] = df
        st.success("✅ Timetable loaded successfully!")
        st.dataframe(df, use_container_width=True)

    else:
        st.info("No file uploaded. Loading default demo timetable instead.")
        default_csv = os.path.join(ROOT, "sample_timetable_with_conflicts.csv")
        df = load_csv(None, default_csv)
        st.session_state["timetable"] = df
        st.dataframe(df, use_container_width=True)

    # --- Download button ---
    if "timetable" in st.session_state:
        df = st.session_state["timetable"]
        st.download_button(
            "Download current timetable (CSV)",
            data=df.to_csv(index=False),
            file_name="current_timetable.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()

