import os
import streamlit as st
import pandas as pd
from engines.conflict_detector import detect_conflicts
from PIL import Image

st.set_page_config(page_title="Conflict Detection", layout="wide")

# --- TITLE + LOGO SIDE BY SIDE ---
col1, col2 = st.columns([8, 2])  # same ratio as before
with col1:
    st.title("🚦 Conflict Detection")
with col2:
    logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    else:
        st.warning("Logo not found at given path!")

# --- Load timetable from session_state ---
if "timetable" not in st.session_state:
    st.warning("⚠️ Please upload a timetable first from **Page 1**.")
else:
    df = st.session_state["timetable"]

    st.subheader("📋 Uploaded Timetable")
    st.dataframe(df, use_container_width=True)

    # Detect conflicts
    conflicts = detect_conflicts(df)

    st.subheader("⚠️ Detected Conflicts")
    if conflicts.empty:
        st.success("✅ No conflicts detected in the current timetable.")
    else:
        # Show conflict table with colored rows
        def color_rows(row):
            if row["type"] == "BlockConflict":
                return ["background-color: #fdd"] * len(row)
            elif row["type"] == "PlatformConflict":
                return ["background-color: #ffd"] * len(row)
            elif row["type"] == "HeadwayViolation":
                return ["background-color: #dfd"] * len(row)
            else:
                return [""] * len(row)

        st.dataframe(
            conflicts.style.apply(color_rows, axis=1),
            use_container_width=True
        )

        # Save conflicts to session state for later optimization
        st.session_state["conflicts"] = conflicts

