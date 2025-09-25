# app.py
import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Railway Simulation", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("RailSimulate Navigation")
st.sidebar.markdown("""
Use the sidebar to switch between pages:
1. Upload Timetable  
2. Conflict Detection  
3. Optimization  
4. Simulation  
5. Dashboard  
6. Comprehensive Reporting
""")

# --- Top header with logo on right ---
col1, col2 = st.columns([8, 2])
with col1:
    st.title("🚆 RailSimulate Prototype")
with col2:
    logo_path = r"C:\Users\123an\Downloads\pravah.jpg"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    else:
        st.warning("Logo not found at given path!")

# --- Landing Page Content ---
st.markdown("""
Welcome to **RailSimulate** – a prototype for Railway Timetable  
**Simulation, Conflict Detection, Optimization, and Visualization**.
""")

# --- Centered Login Card ---
st.markdown("### 🔒 Login Administration")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div style='
            background-color:#c0edfc;  
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        '>
            <h3 style='text-align:center;'>Section Controller</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    id_input = st.text_input("ID", placeholder="Enter your ID")
    pass_input = st.text_input("Security Key", type="password", placeholder="Enter your Security Key")
    
    st.markdown("<div style='text-align:right;'><a href='#'>Forgot Password?</a></div>", unsafe_allow_html=True)
    
    st.button("Login", key="fake_login", type="primary")

