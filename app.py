import streamlit as st
import json
import tempfile
import os
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import ee
import traceback
import base64

# Custom CSS for Clean Green & Black TypeScript/React Style
st.markdown("""
<style>
    /* Base styling */
    .stApp {
        background: #000000;
        color: #ffffff;
    }
    
    /* Remove Streamlit default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Green & Black Theme */
    :root {
        --primary-green: #00ff88;
        --accent-green: #00cc6a;
        --primary-black: #000000;
        --card-black: #0a0a0a;
        --secondary-black: #111111;
        --border-gray: #222222;
        --text-white: #ffffff;
        --text-gray: #999999;
        --text-light-gray: #cccccc;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 600;
        letter-spacing: -0.025em;
        color: var(--text-white) !important;
    }
    
    h1 {
        font-size: 2rem !important;
        background: linear-gradient(90deg, var(--primary-green), var(--accent-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        color: var(--primary-green) !important;
    }
    
    h3 {
        font-size: 1.25rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Layout Container */
    .main-container {
        display: flex;
        gap: 20px;
        max-width: 1800px;
        margin: 0 auto;
    }
    
    .sidebar-container {
        width: 320px;
        flex-shrink: 0;
    }
    
    .content-container {
        flex: 1;
        min-width: 0;
    }
    
    /* Cards */
    .card {
        background: var(--card-black);
        border: 1px solid var(--border-gray);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        border-color: var(--primary-green);
    }
    
    .card-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-gray);
    }
    
    .card-title .icon {
        width: 32px;
        height: 32px;
        background: rgba(0, 255, 136, 0.1);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary-green);
        font-size: 16px;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, var(--primary-green), var(--accent-green));
        color: var(--primary-black) !important;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        margin: 5px 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
    }
    
    /* Primary button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, var(--primary-green), var(--accent-green)) !important;
        color: var(--primary-black) !important;
    }
    
    /* Secondary button */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: transparent !important;
        color: var(--primary-green) !important;
        border: 1px solid var(--primary-green) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--secondary-black) !important;
        border: 1px solid var(--border-gray) !important;
        color: var(--text-white) !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2) !important;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: var(--text-light-gray) !important;
        font-weight: 500;
        font-size: 14px;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, var(--primary-green), var(--accent-green)) !important;
    }
    
    .stSlider > div > div > div > div {
        background: var(--primary-green) !important;
        border: 3px solid var(--primary-green) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: var(--secondary-black) !important;
        border: 1px solid var(--border-gray) !important;
    }
    
    /* Multi-select */
    .stMultiSelect > div > div > div {
        background: var(--secondary-black) !important;
        border: 1px solid var(--border-gray) !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        border: 2px dashed var(--border-gray) !important;
        border-radius: 6px !important;
        background: var(--secondary-black) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background: var(--card-black);
        padding: 5px;
        border-radius: 8px;
        border: 1px solid var(--border-gray);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        background: transparent;
        color: var(--text-gray);
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 14px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-green) !important;
        color: var(--primary-black) !important;
    }
    
    /* Dataframes */
    .dataframe {
        background: var(--card-black) !important;
        border: 1px solid var(--border-gray) !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: var(--secondary-black) !important;
        color: var(--primary-green) !important;
        font-weight: 600 !important;
        border-color: var(--border-gray) !important;
    }
    
    .dataframe td {
        color: var(--text-light-gray) !important;
        border-color: var(--border-gray) !important;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        background: rgba(0, 255, 136, 0.1);
        color: var(--primary-green);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Alert boxes */
    .alert {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid;
        background: var(--card-black);
        font-size: 14px;
    }
    
    .alert-success {
        border-color: rgba(0, 255, 136, 0.3);
        color: var(--primary-green);
    }
    
    .alert-warning {
        border-color: rgba(255, 170, 0, 0.3);
        color: #ffaa00;
    }
    
    .alert-error {
        border-color: rgba(255, 68, 68, 0.3);
        color: #ff4444;
    }
    
    /* Compact form layout */
    .form-row {
        margin-bottom: 15px;
    }
    
    .form-label {
        color: var(--text-gray);
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 5px;
        display: block;
    }
    
    /* Map container */
    .map-container {
        border: 1px solid var(--border-gray);
        border-radius: 10px;
        overflow: hidden;
        height: 600px;
    }
    
    /* 3D Globe container */
    .globe-container {
        border: 1px solid var(--border-gray);
        border-radius: 10px;
        overflow: hidden;
        height: 600px;
        background: #000;
        position: relative;
    }
    
    /* Mapbox specific */
    #map {
        width: 100%;
        height: 100%;
        border-radius: 8px;
    }
    
    .mapboxgl-popup {
        max-width: 300px;
    }
    
    .mapboxgl-popup-content {
        background: var(--card-black);
        color: var(--text-white);
        border: 1px solid var(--border-gray);
        border-radius: 8px;
        padding: 15px;
    }
    
    .mapboxgl-popup-content h3 {
        color: var(--primary-green);
        margin: 0 0 10px 0;
        font-size: 16px;
    }
    
    .mapboxgl-popup-content p {
        margin: 0;
        color: var(--text-light-gray);
        font-size: 14px;
    }
    
    .mapboxgl-popup-close-button {
        color: var(--text-white);
        font-size: 16px;
        padding: 8px;
    }
    
    .mapboxgl-ctrl-group {
        background: var(--card-black) !important;
        border: 1px solid var(--border-gray) !important;
    }
    
    .mapboxgl-ctrl button {
        background-color: transparent !important;
    }
    
    /* Section divider */
    .section-divider {
        height: 1px;
        background: var(--border-gray);
        margin: 25px 0;
    }
    
    /* Compact header */
    .compact-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    /* Info panel */
    .info-panel {
        background: var(--card-black);
        border: 1px solid var(--border-gray);
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
    }
    
    .info-item {
        margin-bottom: 10px;
    }
    
    .info-label {
        color: var(--text-gray);
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 2px;
    }
    
    .info-value {
        color: var(--text-white);
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Analysis status */
    .analysis-status {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 15px;
        background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.2);
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* View toggle */
    .view-toggle {
        display: flex;
        background: var(--card-black);
        border-radius: 8px;
        padding: 4px;
        border: 1px solid var(--border-gray);
        margin-bottom: 15px;
    }
    
    .view-option {
        flex: 1;
        padding: 8px 12px;
        text-align: center;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        border-radius: 6px;
        transition: all 0.2s;
        color: var(--text-gray);
    }
    
    .view-option.active {
        background: var(--primary-green);
        color: var(--primary-black);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Earth Engine Auto-Authentication with Service Account
def auto_initialize_earth_engine():
    """Automatically initialize Earth Engine with service account credentials"""
    try:
        service_account_info = {
            "type": "service_account",
            "project_id": "citric-hawk-457513-i6",
            "private_key_id": "8984179a69969591194d8f8097e48cd9789f5ea2",
            "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDFQOtXKWE+7mEY
JUTNzx3h+QvvDCvZ2B6XZTofknuAFPW2LqAzZustznJJFkCmO3Nutct+W/iDQCG0
1DjOQcbcr/jWr+mnRLVOkUkQc/kzZ8zaMQqU8HpXjS1mdhpsrbUaRKoEgfo3I3Bp
dFcJ/caC7TSr8VkGnZcPEZyXVsj8dLSEzomdkX+mDlJlgCrNfu3Knu+If5lXh3Me
SKiMWsfMnasiv46oD4szBzg6HLgoplmNka4NiwfeM7qROYnCd+5conyG8oiU00Xe
zC2Ekzo2dWsCw4zIJD6IdAcvgdrqH63fCqDFmAjEBZ69h8fWrdnsq56dAIpt0ygl
P9ADiRbVAgMBAAECggEALO7AnTqBGy2AgxhMP8iYEUdiu0mtvIIxV8HYl2QOC2ta
3GzrE8J0PJs8J99wix1cSmIRkH9hUP6dHvy/0uYjZ1aTi84HHtH1LghE2UFdySKy
RJqqwyozaDmx15b8Jnj8Wdc91miIR6KkQvVcNVuwalcf6jIAWlQwGp/jqIq9nloN
eld6xNbEmacORz1qT+4/uxOE05mrrZHC4kIKtswi8Io4ExVe61VxXsXWSHrMCGz0
TiSGr2ORSlRWC/XCGCu7zFIJU/iw6BiNsxryk6rjqQrcAtmoFTFx0fWbjYkG1DDs
k/9Dov1gyx0OtEyX8beoaf0Skcej4zdfeuido2A1sQKBgQD4IrhFn50i4/pa9sk1
g7v1ypGTrVA3pfvj6c7nTgzj9oyJnlU3WJwCqLw1cTFiY84+ekYP15wo8xsu5VZd
YLzOKEg3B8g899Ge14vZVNd6cNfRyMk4clGrDwGnZ4OAQkdsT/AyaCGRIcyu9njA
xdmWa+6VPMG7U65f/656XGwkBQKBgQDLgVyRE2+r1XCY+tdtXtga9sQ4LoiYHzD3
eDHe056qmwk8jf1A1HekILnC1GyeaKkOUd4TEWhVBgQpsvtC4Z2zPXlWR8N7SwNu
SFAhy3OnHTZQgrRWFA8eBjeI0YoXmk5m6uMQ7McmDlFxxXenFi+qSl3Cu4aGGuOy
cfyWMbTwkQKBgAoKfaJznww2ZX8g1WuQ9R4xIEr1jHV0BglnALRjeCoRZAZ9nb0r
nMSOx27yMallmIb2s7cYZn1RuRvgs+n7bCh7gNCZRAUTkiv3VPVqdX3C6zjWAy6B
kcR2Sv7XNX8PL4y2f2XKyPDyiTHbT2+dkfyASZtIZh6KeFfyJMFW1BlxAoGAAeG6
V2UUnUQl/GQlZc+AtA8gFVzoym9PZppn66WNTAqO9U5izxyn1o6u6QxJzNUu6wD6
yrZYfqDFnRUYma+4Y5Xn71JOjm9NItHsW8Oj2CG/BNOQk1MwKJjqHovBeSJmIzF8
1AU8ei+btS+cQaFE45A4ebp+LfNFs7q2GTVwdOECgYEAtHkMqigOmZdR3QAcZTjL
3aeOMGVHB2pHYosTgslD9Yp+hyVHqSdyCplHzWB3d8roIecW4MEb0mDxlaTdZfmR
dtBYiTzMxLezHsRZ4KP4NtGAE3iTL1b6DXuoI84+H/HaQ1EB79+YV9ZTAabt1b7o
e5aU1RW6tlG8nzHHwK2FeyI=
-----END PRIVATE KEY-----""",
            "client_email": "cc-365@citric-hawk-457513-i6.iam.gserviceaccount.com",
            "client_id": "105264622264803277310",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cc-365%40citric-hawk-457513-i6.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }
        
        credentials = ee.ServiceAccountCredentials(
            service_account_info['client_email'],
            key_data=json.dumps(service_account_info)
        )
        
        ee.Initialize(credentials, project='citric-hawk-457513-i6')
        return True
    except Exception as e:
        st.error(f"Earth Engine auto-initialization failed: {str(e)}")
        return False

# Try to auto-initialize Earth Engine on app start
if 'ee_auto_initialized' not in st.session_state:
    with st.spinner("Initializing Earth Engine..."):
        if auto_initialize_earth_engine():
            st.session_state.ee_auto_initialized = True
            st.session_state.ee_initialized = True
        else:
            st.session_state.ee_auto_initialized = False
            st.session_state.ee_initialized = False

# Initialize session state for map
if 'map_view' not in st.session_state:
    st.session_state.map_view = "satellite"  # "satellite", "street", "terrain", "dark"

# Page configuration
st.set_page_config(
    page_title="Khisba GIS - Interactive Global Vegetation Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'ee_initialized' not in st.session_state:
    st.session_state.ee_initialized = False
if 'credentials_uploaded' not in st.session_state:
    st.session_state.credentials_uploaded = False
if 'selected_geometry' not in st.session_state:
    st.session_state.selected_geometry = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Authentication check
if not st.session_state.authenticated:
    st.markdown("""
    <div class="main-container">
        <div class="content-container" style="max-width: 500px; margin: 100px auto;">
            <div class="card">
                <h1 style="text-align: center; margin-bottom: 10px;">🌍 KHISBA GIS</h1>
                <p style="text-align: center; color: #999999; margin-bottom: 30px;">Interactive Global Vegetation Analytics</p>
                
                <div class="alert alert-warning" style="text-align: center;">
                    🔐 Authentication Required
                </div>
                
                <div class="form-row">
                    <div class="form-label">Password</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("", type="password", placeholder="Enter admin password", label_visibility="collapsed")
        
        if st.button("🔓 Sign In", type="primary", use_container_width=True):
            if password == "admin":
                st.session_state.authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password")
    
    st.markdown("""
    <div class="main-container">
        <div class="content-container" style="max-width: 500px; margin: 30px auto;">
            <div class="card">
                <p style="text-align: center; color: #00ff88; font-weight: 600; margin-bottom: 10px;">Demo Access</p>
                <p style="text-align: center; color: #999999;">Use <strong>admin</strong> / <strong>admin</strong> for demo</p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    <span class="status-badge">Interactive Globe</span>
                    <span class="status-badge">GIS Analytics</span>
                    <span class="status-badge">Satellite Data</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Main Dashboard Layout
st.markdown("""
<div class="compact-header">
    <div>
        <h1>🌍 KHISBA GIS</h1>
        <p style="color: #999999; margin: 0; font-size: 14px;">Interactive Global Vegetation Indices Analytics</p>
    </div>
    <div style="display: flex; gap: 10px;">
        <span class="status-badge">Connected</span>
        <span class="status-badge">Interactive Globe</span>
        <span class="status-badge">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Map Style Toggle
col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 2, 1])
with col_toggle2:
    st.markdown('<div class="view-toggle">', unsafe_allow_html=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        if st.button("🛰️ Satellite", use_container_width=True, key="satellite_btn"):
            st.session_state.map_view = "satellite"
            st.rerun()
    with col_b:
        if st.button("🗺️ Streets", use_container_width=True, key="streets_btn"):
            st.session_state.map_view = "street"
            st.rerun()
    with col_c:
        if st.button("🏔️ Terrain", use_container_width=True, key="terrain_btn"):
            st.session_state.map_view = "terrain"
            st.rerun()
    with col_d:
        if st.button("🌙 Dark", use_container_width=True, key="dark_btn"):
            st.session_state.map_view = "dark"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Create main layout containers
col1, col2 = st.columns([0.25, 0.75], gap="large")

# LEFT SIDEBAR - All controls
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">🌍</div><h3 style="margin: 0;">Area Selection</h3></div>', unsafe_allow_html=True)
    
    # Import the helper functions
    try:
        from earth_engine_utils import get_admin_boundaries, get_boundary_names
        from vegetation_indices import mask_clouds, add_vegetation_indices
    except ImportError as e:
        st.error(f"Error importing helper modules: {str(e)}")
        st.info("Please ensure earth_engine_utils.py and vegetation_indices.py are in the same directory")
        st.stop()
    
    if st.session_state.ee_initialized:
        # Country selection
        try:
            countries_fc = get_admin_boundaries(0)
            if countries_fc is not None:
                country_names = get_boundary_names(countries_fc, 0)
                selected_country = st.selectbox(
                    "Country",
                    options=[""] + country_names,
                    help="Choose a country for analysis",
                    key="country_select"
                )
            else:
                st.error("Failed to load countries data")
                selected_country = ""
        except Exception as e:
            st.error(f"Error loading countries: {str(e)}")
            selected_country = ""
        
        # Admin1 selection
        selected_admin1 = ""
        if selected_country and countries_fc is not None:
            try:
                country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first()
                country_code = country_feature.get('ADM0_CODE').getInfo()
                
                admin1_fc = get_admin_boundaries(1, country_code)
                if admin1_fc is not None:
                    admin1_names = get_boundary_names(admin1_fc, 1)
                    selected_admin1 = st.selectbox(
                        "State/Province",
                        options=[""] + admin1_names,
                        help="Choose a state or province",
                        key="admin1_select"
                    )
            except Exception as e:
                st.error(f"Error loading admin1: {str(e)}")
        
        # Admin2 selection
        selected_admin2 = ""
        if selected_admin1 and 'admin1_fc' in locals() and admin1_fc is not None:
            try:
                admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
                admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                
                admin2_fc = get_admin_boundaries(2, None, admin1_code)
                if admin2_fc is not None:
                    admin2_names = get_boundary_names(admin2_fc, 2)
                    selected_admin2 = st.selectbox(
                        "Municipality",
                        options=[""] + admin2_names,
                        help="Choose a municipality",
                        key="admin2_select"
                    )
            except Exception as e:
                st.error(f"Error loading admin2: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Parameters Card
    if selected_country:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">⚙️</div><h3 style="margin: 0;">Analysis Settings</h3></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            start_date = st.date_input(
                "Start Date",
                value=datetime(2023, 1, 1),
                help="Start date for analysis",
                key="start_date"
            )
        with col_b:
            end_date = st.date_input(
                "End Date",
                value=datetime(2023, 12, 31),
                help="End date for analysis",
                key="end_date"
            )
        
        collection_choice = st.selectbox(
            "Satellite Source",
            options=["Sentinel-2", "Landsat-8"],
            help="Choose satellite collection",
            key="satellite_select"
        )
        
        cloud_cover = st.slider(
            "Max Cloud Cover (%)",
            min_value=0,
            max_value=100,
            value=20,
            help="Maximum cloud cover percentage",
            key="cloud_slider"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Vegetation Indices Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">🌿</div><h3 style="margin: 0;">Vegetation Indices</h3></div>', unsafe_allow_html=True)
        
        available_indices = [
            'NDVI', 'ARVI', 'ATSAVI', 'DVI', 'EVI', 'EVI2', 'GNDVI', 'MSAVI', 'MSI', 'MTVI', 'MTVI2',
            'NDTI', 'NDWI', 'OSAVI', 'RDVI', 'RI', 'RVI', 'SAVI', 'TVI', 'TSAVI', 'VARI', 'VIN', 'WDRVI',
            'GCVI', 'AWEI', 'MNDWI', 'WI', 'ANDWI', 'NDSI', 'nDDI', 'NBR', 'DBSI', 'SI', 'S3', 'BRI',
            'SSI', 'NDSI_Salinity', 'SRPI', 'MCARI', 'NDCI', 'PSSRb1', 'SIPI', 'PSRI', 'Chl_red_edge', 'MARI', 'NDMI'
        ]
        
        selected_indices = st.multiselect(
            "Select Indices",
            options=available_indices,
            default=['NDVI', 'EVI', 'SAVI', 'NDWI'],
            help="Choose vegetation indices to analyze",
            key="indices_select"
        )
        
        col_c, col_d = st.columns(2)
        with col_c:
            if st.button("Select All", use_container_width=True, key="select_all"):
                selected_indices = available_indices
                st.rerun()
        with col_d:
            if st.button("Clear All", use_container_width=True, key="clear_all"):
                selected_indices = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Navigation Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">🚀</div><h3 style="margin: 0;">Quick Navigation</h3></div>', unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            if st.button("🇺🇸 USA", use_container_width=True, key="usa_btn"):
                st.session_state.fly_to_region = "usa"
                st.rerun()
            if st.button("🇪🇺 Europe", use_container_width=True, key="europe_btn"):
                st.session_state.fly_to_region = "europe"
                st.rerun()
        with col_g2:
            if st.button("🇨🇳 Asia", use_container_width=True, key="asia_btn"):
                st.session_state.fly_to_region = "asia"
                st.rerun()
            if st.button("🇧🇷 Americas", use_container_width=True, key="americas_btn"):
                st.session_state.fly_to_region = "americas"
                st.rerun()
        
        if st.button("🌐 Reset View", use_container_width=True, key="reset_btn"):
            st.session_state.fly_to_region = "reset"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Run Analysis Button
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True, key="run_analysis"):
            if not selected_indices:
                st.error("Please select at least one vegetation index")
            else:
                with st.spinner("Running analysis..."):
                    try:
                        # Define collection based on choice
                        if collection_choice == "Sentinel-2":
                            collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                        else:
                            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                        
                        # Filter collection
                        filtered_collection = (collection
                            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                            .filterBounds(st.session_state.selected_geometry)
                            .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', cloud_cover))
                        )
                        
                        # Apply cloud masking and add vegetation indices
                        if collection_choice == "Sentinel-2":
                            processed_collection = (filtered_collection
                                .map(mask_clouds)
                                .map(add_vegetation_indices)
                            )
                        else:
                            processed_collection = filtered_collection.map(add_vegetation_indices)
                        
                        # Calculate time series for selected indices
                        results = {}
                        for index in selected_indices:
                            try:
                                def add_date_and_reduce(image):
                                    reduced = image.select(index).reduceRegion(
                                        reducer=ee.Reducer.mean(),
                                        geometry=st.session_state.selected_geometry.geometry(),
                                        scale=30,
                                        maxPixels=1e9
                                    )
                                    return ee.Feature(None, reduced.set('date', image.date().format()))
                                
                                time_series = processed_collection.map(add_date_and_reduce)
                                time_series_list = time_series.getInfo()
                                
                                dates = []
                                values = []
                                
                                if 'features' in time_series_list:
                                    for feature in time_series_list['features']:
                                        props = feature['properties']
                                        if index in props and props[index] is not None and 'date' in props:
                                            dates.append(props['date'])
                                            values.append(props[index])
                                
                                results[index] = {'dates': dates, 'values': values}
                                
                            except Exception as e:
                                st.warning(f"Could not calculate {index}: {str(e)}")
                                results[index] = {'dates': [], 'values': []}
                        
                        st.session_state.analysis_results = results
                        st.success("✅ Analysis completed!")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")

# MAIN CONTENT AREA - Interactive Mapbox Globe
with col2:
    # Interactive Mapbox Globe
    st.markdown('<div class="card" style="padding: 0;">', unsafe_allow_html=True)
    st.markdown('<div style="padding: 20px 20px 10px 20px;"><h3 style="margin: 0;">Interactive Global Map</h3></div>', unsafe_allow_html=True)
    
    # Map style mapping
    map_styles = {
        "satellite": "mapbox://styles/mapbox/satellite-streets-v12",
        "street": "mapbox://styles/mapbox/streets-v12",
        "terrain": "mapbox://styles/mapbox/outdoors-v12",
        "dark": "mapbox://styles/mapbox/dark-v11"
    }
    
    # Generate HTML for Mapbox interactive globe
    mapbox_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
      <title>KHISBA GIS - Interactive Global Map</title>
      <script src='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js'></script>
      <link href='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css' rel='stylesheet' />
      <style>
        body {{ 
          margin: 0; 
          padding: 0; 
          background: #000000;
        }}
        #map {{ 
          position: absolute; 
          top: 0; 
          bottom: 0; 
          width: 100%; 
          border-radius: 8px;
        }}
        .mapboxgl-popup {{
          max-width: 300px;
        }}
        .mapboxgl-popup-content {{
          background: #0a0a0a;
          color: #ffffff;
          border: 1px solid #222222;
          border-radius: 8px;
          padding: 15px;
          font-family: 'Inter', sans-serif;
        }}
        .mapboxgl-popup-content h3 {{
          color: #00ff88;
          margin: 0 0 10px 0;
          font-size: 16px;
        }}
        .mapboxgl-popup-content p {{
          margin: 0;
          color: #cccccc;
          font-size: 14px;
        }}
        .mapboxgl-popup-close-button {{
          color: #ffffff;
          font-size: 16px;
          padding: 8px;
        }}
        .info-panel {{
          position: absolute;
          top: 20px;
          right: 20px;
          background: rgba(10, 10, 10, 0.9);
          color: white;
          padding: 15px;
          border-radius: 8px;
          border: 1px solid #222222;
          max-width: 250px;
          z-index: 1000;
          font-family: 'Inter', sans-serif;
        }}
        .info-title {{
          color: #00ff88;
          font-weight: 600;
          margin-bottom: 10px;
          font-size: 14px;
        }}
        .info-text {{
          color: #cccccc;
          font-size: 12px;
          line-height: 1.4;
        }}
        .coordinates-display {{
          position: absolute;
          bottom: 20px;
          left: 20px;
          background: rgba(10, 10, 10, 0.9);
          color: white;
          padding: 10px 15px;
          border-radius: 6px;
          border: 1px solid #222222;
          font-family: monospace;
          font-size: 12px;
          z-index: 1000;
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <div class="info-panel">
        <div class="info-title">🌍 KHISBA GIS</div>
        <div class="info-text">
          • Click on markers to fly to locations<br>
          • Drag to rotate the globe<br>
          • Scroll to zoom in/out<br>
          • Right-click to pan
        </div>
      </div>
      <div class="coordinates-display">
        <div>Lat: <span id="lat-display">0.00°</span></div>
        <div>Lon: <span id="lon-display">0.00°</span></div>
      </div>
      
      <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiYnJ5Y2VseW5uMjUiLCJhIjoiY2x1a2lmcHh5MGwycTJrbzZ4YXVrb2E0aiJ9.LXbneMJJ6OosHv9ibtI5XA';

        // Create a new map instance
        const map = new mapboxgl.Map({{
          container: 'map',
          style: '{map_styles[st.session_state.map_view]}',
          center: [-95.7129, 37.0902], // Center of USA
          zoom: 3,
          pitch: 0,
          bearing: 0
        }});

        // Add navigation controls
        map.addControl(new mapboxgl.NavigationControl());

        // Add scale control
        map.addControl(new mapboxgl.ScaleControl({{
          unit: 'metric'
        }}));

        // Add fullscreen control
        map.addControl(new mapboxgl.FullscreenControl());

        // List of major cities with their coordinates and names
        const cities = [
          {{ name: 'New York', coordinates: [-74.006, 40.7128], country: 'USA', info: 'Financial capital of the world' }},
          {{ name: 'Los Angeles', coordinates: [-118.2437, 34.0522], country: 'USA', info: 'Entertainment capital' }},
          {{ name: 'Chicago', coordinates: [-87.6298, 41.8781], country: 'USA', info: 'Windy City' }},
          {{ name: 'Houston', coordinates: [-95.3698, 29.7604], country: 'USA', info: 'Space City' }},
          {{ name: 'Phoenix', coordinates: [-112.074, 33.4484], country: 'USA', info: 'Valley of the Sun' }},
          {{ name: 'Paris', coordinates: [2.3522, 48.8566], country: 'France', info: 'City of Light' }},
          {{ name: 'London', coordinates: [-0.1276, 51.5074], country: 'UK', info: 'Historical capital' }},
          {{ name: 'Tokyo', coordinates: [139.6917, 35.6895], country: 'Japan', info: 'Mega metropolis' }},
          {{ name: 'Beijing', coordinates: [116.4074, 39.9042], country: 'China', info: 'Ancient capital' }},
          {{ name: 'Sydney', coordinates: [151.2093, -33.8688], country: 'Australia', info: 'Harbor city' }},
          {{ name: 'Cairo', coordinates: [31.2357, 30.0444], country: 'Egypt', info: 'Nile Delta' }},
          {{ name: 'Rio de Janeiro', coordinates: [-43.1729, -22.9068], country: 'Brazil', info: 'Carnival city' }},
          {{ name: 'Moscow', coordinates: [37.6173, 55.7558], country: 'Russia', info: 'Red Square' }},
          {{ name: 'Dubai', coordinates: [55.2708, 25.2048], country: 'UAE', info: 'Modern metropolis' }},
          {{ name: 'Singapore', coordinates: [103.8198, 1.3521], country: 'Singapore', info: 'Garden city' }}
        ];

        // Region coordinates for quick navigation
        const regions = {{
          usa: {{ center: [-95.7129, 37.0902], zoom: 3 }},
          europe: {{ center: [15.2551, 54.5260], zoom: 3 }},
          asia: {{ center: [104.1954, 35.8617], zoom: 2 }},
          americas: {{ center: [-58.3816, -14.2350], zoom: 2 }},
          reset: {{ center: [0, 20], zoom: 1 }}
        }};

        // Wait for map to load
        map.on('load', () => {{
          // Add custom markers
          cities.forEach(city => {{
            // Create a custom marker element
            const el = document.createElement('div');
            el.className = 'marker';
            el.style.backgroundColor = '#00ff88';
            el.style.width = '20px';
            el.style.height = '20px';
            el.style.borderRadius = '50%';
            el.style.border = '2px solid #ffffff';
            el.style.boxShadow = '0 0 10px rgba(0, 255, 136, 0.5)';
            el.style.cursor = 'pointer';
            el.style.transition = 'all 0.3s';

            // Add hover effect
            el.addEventListener('mouseenter', () => {{
              el.style.transform = 'scale(1.3)';
              el.style.boxShadow = '0 0 15px rgba(0, 255, 136, 0.8)';
            }});

            el.addEventListener('mouseleave', () => {{
              el.style.transform = 'scale(1)';
              el.style.boxShadow = '0 0 10px rgba(0, 255, 136, 0.5)';
            }});

            // Create a popup
            const popup = new mapboxgl.Popup({{
              offset: 25,
              closeButton: true,
              closeOnClick: false
            }}).setHTML(
              `<h3>${{city.name}}</h3>
               <p><strong>Country:</strong> ${{city.country}}</p>
               <p>${{city.info}}</p>
               <p><strong>Coordinates:</strong><br>
               Lat: ${{city.coordinates[1].toFixed(4)}}°<br>
               Lon: ${{city.coordinates[0].toFixed(4)}}°</p>`
            );

            // Create marker
            const marker = new mapboxgl.Marker(el)
              .setLngLat(city.coordinates)
              .setPopup(popup)
              .addTo(map);

            // Add click event for fly-to animation
            el.addEventListener('click', (e) => {{
              e.stopPropagation();
              
              // First fly out to zoom all the way out
              map.flyTo({{
                center: city.coordinates,
                zoom: 1,
                speed: 1,
                curve: 1.6,
                easing: (t) => t,
                essential: true
              }});

              // Once the first flyTo is done, zoom back into the marker
              map.once('moveend', () => {{
                map.flyTo({{
                  center: city.coordinates,
                  zoom: 10,
                  speed: 0.8,
                  curve: 0.8,
                  easing: (t) => t * (2 - t),
                  essential: true
                }});
              }});

              // Open the popup
              popup.addTo(map);
            }});
          }});

          // Add event listener for mouse move to show coordinates
          map.on('mousemove', (e) => {{
            document.getElementById('lat-display').textContent = e.lngLat.lat.toFixed(2) + '°';
            document.getElementById('lon-display').textContent = e.lngLat.lng.toFixed(2) + '°';
          }});

          // Listen for messages from Streamlit to fly to regions
          window.addEventListener('message', (event) => {{
            if (event.data && event.data.type === 'FLY_TO_REGION') {{
              const region = event.data.region;
              if (regions[region]) {{
                const {{ center, zoom }} = regions[region];
                
                // Fly to region with animation
                map.flyTo({{
                  center: center,
                  zoom: zoom,
                  duration: 2000,
                  essential: true
                }});
              }}
            }}
          }});

          // Trigger initial region fly if specified
          const initialRegion = localStorage.getItem('flyToRegion');
          if (initialRegion && regions[initialRegion]) {{
            const {{ center, zoom }} = regions[initialRegion];
            map.flyTo({{
              center: center,
              zoom: zoom,
              duration: 2000,
              essential: true
            }});
            localStorage.removeItem('flyToRegion');
          }}
        }});

        // Handle region fly from Streamlit
        function flyToRegion(region) {{
          if (regions[region]) {{
            const {{ center, zoom }} = regions[region];
            
            map.flyTo({{
              center: center,
              zoom: zoom,
              duration: 2000,
              essential: true
            }});
          }}
        }}
      </script>
    </body>
    </html>
    """
    
    # Display the Mapbox HTML
    st.components.v1.html(mapbox_html, height=550)
    
    # Handle region navigation from Streamlit
    if 'fly_to_region' in st.session_state and st.session_state.fly_to_region:
        region = st.session_state.fly_to_region
        st.markdown(f"""
        <script>
            window.parent.postMessage({{
                type: 'FLY_TO_REGION',
                region: '{region}'
            }}, '*');
        </script>
        """, unsafe_allow_html=True)
        # Clear after sending
        st.session_state.fly_to_region = None
    
    # Area info at bottom of map
    if selected_country:
        try:
            # Determine geometry
            if selected_admin2 and 'admin2_fc' in locals() and admin2_fc is not None:
                geometry = admin2_fc.filter(ee.Filter.eq('ADM2_NAME', selected_admin2))
                area_name = f"{selected_admin2}, {selected_admin1}, {selected_country}"
                area_level = "Municipality"
            elif selected_admin1 and 'admin1_fc' in locals() and admin1_fc is not None:
                geometry = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1))
                area_name = f"{selected_admin1}, {selected_country}"
                area_level = "State/Province"
            else:
                geometry = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country))
                area_name = selected_country
                area_level = "Country"
            
            bounds = geometry.geometry().bounds().getInfo()
            coords = bounds['coordinates'][0]
            lats = [coord[1] for coord in coords]
            lons = [coord[0] for coord in coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
            
            st.session_state.selected_geometry = geometry
            
            st.markdown(f"""
            <div class="info-panel">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div class="info-item">
                        <div class="info-label">Study Area</div>
                        <div class="info-value">{area_name}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Level</div>
                        <div class="info-value" style="color: #00ff88;">{area_level}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Coordinates</div>
                        <div class="info-value">{center_lat:.4f}°, {center_lon:.4f}°</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Status</div>
                        <div class="info-value" style="color: #00ff88;">Ready for Analysis</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error loading area info: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Results Section
    if st.session_state.analysis_results:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Results Header
        st.markdown('<div class="compact-header"><h3>Analysis Results</h3><span class="status-badge">Complete</span></div>', unsafe_allow_html=True)
        
        results = st.session_state.analysis_results
        
        # Summary Statistics
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📊</div><h3 style="margin: 0;">Summary Statistics</h3></div>', unsafe_allow_html=True)
        
        summary_data = []
        for index, data in results.items():
            if data['values']:
                values = [v for v in data['values'] if v is not None]
                if values:
                    summary_data.append({
                        'Index': index,
                        'Mean': round(sum(values) / len(values), 4),
                        'Min': round(min(values), 4),
                        'Max': round(max(values), 4),
                        'Count': len(values)
                    })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📈</div><h3 style="margin: 0;">Vegetation Analytics</h3></div>', unsafe_allow_html=True)
        
        # Chart controls
        col_x, col_y = st.columns([3, 1])
        with col_x:
            indices_to_plot = st.multiselect(
                "Select Indices to Plot",
                options=list(results.keys()),
                default=list(results.keys())[:4] if len(results) >= 4 else list(results.keys()),
                help="Choose vegetation indices to plot",
                key="chart_indices"
            )
        with col_y:
            chart_style = st.selectbox(
                "Chart Style",
                ["Professional", "Statistical", "Area"],
                help="Select chart visualization style",
                key="chart_style"
            )
        
        # Generate charts
        if indices_to_plot:
            for index in indices_to_plot:
                data = results[index]
                if data['dates'] and data['values']:
                    try:
                        dates = [datetime.fromisoformat(d.replace('Z', '+00:00')) for d in data['dates']]
                        values = [v for v in data['values'] if v is not None]
                        
                        if dates and values and len(dates) == len(values):
                            df = pd.DataFrame({'Date': dates, 'Value': values})
                            df = df.sort_values('Date')
                            
                            # Calculate analytical metrics
                            df['MA_5'] = df['Value'].rolling(window=min(5, len(df))).mean()
                            df['MA_10'] = df['Value'].rolling(window=min(10, len(df))).mean()
                            df['Value_Change'] = df['Value'].pct_change()
                            
                            # Create chart
                            fig = go.Figure()
                            
                            current_value = df['Value'].iloc[-1] if len(df) > 0 else 0
                            prev_value = df['Value'].iloc[-2] if len(df) > 1 else current_value
                            is_increasing = current_value >= prev_value
                            
                            if chart_style == "Professional":
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['Value'],
                                    mode='lines',
                                    name=f'{index} Index',
                                    line=dict(color='#00ff88' if is_increasing else '#ff4444', width=3),
                                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Value: %{y:.4f}<extra></extra>'
                                ))
                            elif chart_style == "Statistical":
                                df['Upper_Bound'] = df['Value'] * 1.05
                                df['Lower_Bound'] = df['Value'] * 0.95
                                
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['Upper_Bound'],
                                    mode='lines',
                                    line=dict(width=0),
                                    showlegend=False,
                                    hoverinfo='skip'
                                ))
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['Lower_Bound'],
                                    mode='lines',
                                    line=dict(width=0),
                                    fill='tonexty',
                                    fillcolor='rgba(0,255,136,0.1)',
                                    name='Confidence Band',
                                    hoverinfo='skip'
                                ))
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['Value'],
                                    mode='lines+markers',
                                    name=f'{index} Index',
                                    line=dict(color='#00ff88', width=2),
                                    marker=dict(size=4)
                                ))
                            elif chart_style == "Area":
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['Value'],
                                    fill='tozeroy',
                                    mode='lines',
                                    name=f'{index} Index',
                                    line=dict(color='#00ff88' if is_increasing else '#ff4444', width=2),
                                    fillcolor=f"rgba({'0,255,136' if is_increasing else '255,68,68'}, 0.3)"
                                ))
                            
                            # Add moving averages
                            if len(df) >= 5:
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['MA_5'],
                                    mode='lines',
                                    name='MA 5-day',
                                    line=dict(color='#ffaa00', width=1, dash='dot'),
                                    opacity=0.7
                                ))
                            
                            if len(df) >= 10:
                                fig.add_trace(go.Scatter(
                                    x=df['Date'], 
                                    y=df['MA_10'],
                                    mode='lines',
                                    name='MA 10-day',
                                    line=dict(color='#aa00ff', width=1, dash='dash'),
                                    opacity=0.7
                                ))
                            
                            # Update layout
                            fig.update_layout(
                                title=f'{index} - Vegetation Analysis',
                                plot_bgcolor='#0a0a0a',
                                paper_bgcolor='#0a0a0a',
                                font=dict(color='#ffffff'),
                                xaxis=dict(
                                    gridcolor='#222222',
                                    zerolinecolor='#222222',
                                    tickcolor='#444444',
                                    title_font_color='#ffffff'
                                ),
                                yaxis=dict(
                                    gridcolor='#222222',
                                    zerolinecolor='#222222',
                                    tickcolor='#444444',
                                    title_font_color='#ffffff'
                                ),
                                legend=dict(
                                    bgcolor='rgba(0,0,0,0.5)',
                                    bordercolor='#222222',
                                    borderwidth=1
                                ),
                                hovermode='x unified',
                                height=350,
                                margin=dict(t=50, b=50, l=50, r=50)
                            )
                            
                            # Display chart
                            st.plotly_chart(fig, use_container_width=True)
                            
                    except Exception as e:
                        st.error(f"Error creating chart for {index}: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">💾</div><h3 style="margin: 0;">Data Export</h3></div>', unsafe_allow_html=True)
        
        if st.button("📥 Download Results as CSV", type="primary", use_container_width=True, key="export_csv"):
            export_data = []
            for index, data in results.items():
                for date, value in zip(data['dates'], data['values']):
                    if value is not None:
                        export_data.append({
                            'Date': date,
                            'Index': index,
                            'Value': value
                        })
            
            if export_data:
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="Download CSV File",
                    data=csv,
                    file_name=f"vegetation_indices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for export")
        st.markdown('</div>', unsafe_allow_html=True)

# Status indicators at bottom
if not st.session_state.ee_initialized:
    st.markdown('<div class="alert alert-warning">👆 Earth Engine initialization required. Please upload credentials.</div>', unsafe_allow_html=True)
elif st.session_state.selected_geometry is None:
    st.markdown('<div class="alert alert-warning">👆 Please select a study area to begin analysis.</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="section-divider"></div>
<div style="text-align: center; color: #666666; font-size: 12px; padding: 20px 0;">
    <p style="margin: 5px 0;">KHISBA GIS • Interactive Global Vegetation Analytics Platform</p>
    <p style="margin: 5px 0;">Created by Taibi Farouk Djilali • Clean Green & Black Design</p>
    <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
        <span class="status-badge">Mapbox GL JS</span>
        <span class="status-badge">Earth Engine</span>
        <span class="status-badge">Streamlit</span>
        <span class="status-badge">Interactive Globe</span>
    </div>
</div>
""", unsafe_allow_html=True)
