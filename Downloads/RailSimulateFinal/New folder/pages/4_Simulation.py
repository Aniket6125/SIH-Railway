import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Simulation", layout="wide")

# --- TITLE + LOGO SIDE BY SIDE ---
col1, col2 = st.columns([8, 2])
with col1:
    st.title("🚆 Railway Simulation")
with col2:
    logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    else:
        st.warning("Logo not found at given path!")

# --- Load HTML simulation UI ---
html_file = os.path.join("static", "simulation.html")
if not os.path.exists(html_file):
    st.error("❌ simulation.html file not found in static/ folder")
else:
    # Choose timetable
    if "optimized_timetable" in st.session_state:
        timetable_choice = st.radio(
            "Select timetable for simulation:",
            ("Original", "Optimized"),
            index=1
        )
    else:
        timetable_choice = st.radio(
            "Select timetable for simulation:",
            ("Original",),
            index=0
        )

    # Pick correct timetable
    if timetable_choice == "Optimized":
        timetable = st.session_state["optimized_timetable"]
    else:
        timetable = st.session_state.get("timetable")

    if timetable is None:
        st.warning("⚠️ Please upload timetable in Page 1 first.")
    else:
        st.subheader("📋 Timetable Used in Simulation")
        st.dataframe(timetable, use_container_width=True)

        st.subheader("▶️ Run Simulation")

        if st.button("Start Simulation", type="primary"):
            # Embed simulation.html inside Streamlit
            with open(html_file, "r", encoding="utf-8") as f:
                html_code = f.read()

            st.components.v1.html(html_code, height=600, scrolling=True)
            st.success(f"✅ Simulation started using **{timetable_choice}** timetable!")
