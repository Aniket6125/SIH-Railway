import os
import streamlit as st
import pandas as pd
from engines.optimizer import optimize_timetable
from PIL import Image

st.set_page_config(page_title="Optimization", layout="wide")

# --- TITLE + LOGO SIDE BY SIDE ---
col1, col2 = st.columns([8, 2])  # same ratio as before
with col1:
    st.title("🛠️ Timetable Optimization")
with col2:
    logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    else:
        st.warning("Logo not found at given path!")

# --- Ensure conflicts + timetable exist ---
if "timetable" not in st.session_state:
    st.warning("⚠️ Please upload a timetable first (Page 1).")
elif "conflicts" not in st.session_state:
    st.warning("⚠️ Please run Conflict Detection first (Page 2).")
else:
    timetable = st.session_state["timetable"]
    conflicts = st.session_state["conflicts"]

    st.subheader("⚠️ Detected Conflicts")
    if conflicts.empty:
        st.success("✅ No conflicts found. Nothing to optimize.")
    else:
        st.dataframe(conflicts, use_container_width=True)

        st.subheader("🔧 Resolve Conflicts")
        if st.button("Run Optimization", type="primary"):
            optimized_df, changes = optimize_timetable(timetable, conflicts)

            # Save optimized timetable
            st.session_state["optimized_timetable"] = optimized_df

            st.success("✅ Conflicts resolved and timetable optimized!")

            # ---- Before vs After ----
            st.subheader("📊 Comparison: Before vs After Optimization")
            col1, col2 = st.columns(2)

            with col1:
                st.write("### 🕑 Original Timetable")
                st.dataframe(timetable, use_container_width=True)

            with col2:
                st.write("### 🚀 Optimized Timetable")
                st.dataframe(optimized_df, use_container_width=True)

            # ---- Show changes explicitly ----
            if changes:
                st.subheader("🔍 Adjustments Made")
                changes_df = pd.DataFrame(changes)
                st.table(changes_df)

            # Download option
            csv = optimized_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Optimized Timetable",
                csv,
                "optimized_timetable.csv",
                "text/csv"
            )
