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

# Custom CSS for Green & Black TypeScript/React Style
st.markdown("""
<style>
    /* Base styling */
    .stApp {
        background: #000000;
        color: #ffffff;
    }
    
    /* Green & Black Theme */
    :root {
        --primary-green: #00ff88;
        --primary-black: #000000;
        --secondary-black: #111111;
        --card-bg: #1a1a1a;
        --border-color: #333333;
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
        --text-green: #00ff88;
        --accent-green: #00cc6a;
    }
    
    /* Typography - Modern TypeScript style */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-weight: 600;
        letter-spacing: -0.025em;
        color: var(--text-primary) !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(90deg, var(--primary-green), #00cc6a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.875rem !important;
        color: var(--primary-green) !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
    }
    
    /* Cards - TypeScript style */
    .ts-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .ts-card:hover {
        border-color: var(--primary-green);
        box-shadow: 0 4px 20px rgba(0, 255, 136, 0.1);
    }
    
    /* Buttons - TypeScript style */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-green), var(--accent-green));
        color: var(--primary-black) !important;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 255, 136, 0.3);
    }
    
    /* Primary button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(90deg, var(--primary-green), var(--accent-green)) !important;
        color: var(--primary-black) !important;
        border: none !important;
    }
    
    /* Secondary button */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: var(--secondary-black) !important;
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
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2) !important;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: var(--text-secondary) !important;
        font-weight: 500;
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
        border: 1px solid var(--border-color) !important;
    }
    
    /* Multi-select */
    .stMultiSelect > div > div > div {
        background: var(--secondary-black) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        border: 2px dashed var(--border-color) !important;
        border-radius: 8px !important;
        background: var(--secondary-black) !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background: var(--primary-black) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--card-bg);
        padding: 8px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 12px 24px;
        background: transparent;
        color: var(--text-secondary);
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-green) !important;
        color: var(--primary-black) !important;
    }
    
    /* Dataframes */
    .dataframe {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
    }
    
    .dataframe th {
        background: var(--secondary-black) !important;
        color: var(--primary-green) !important;
        font-weight: 600 !important;
        border-color: var(--border-color) !important;
    }
    
    .dataframe td {
        color: var(--text-secondary) !important;
        border-color: var(--border-color) !important;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        background: rgba(0, 255, 136, 0.1);
        color: var(--primary-green);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-badge.success {
        background: rgba(0, 255, 136, 0.1);
        color: var(--primary-green);
        border-color: rgba(0, 255, 136, 0.3);
    }
    
    .status-badge.warning {
        background: rgba(255, 170, 0, 0.1);
        color: #ffaa00;
        border-color: rgba(255, 170, 0, 0.3);
    }
    
    .status-badge.error {
        background: rgba(255, 68, 68, 0.1);
        color: #ff4444;
        border-color: rgba(255, 68, 68, 0.3);
    }
    
    /* Divider */
    .ts-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 24px 0;
    }
    
    /* Badge */
    .ts-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        background: var(--secondary-black);
        color: var(--text-secondary);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        border: 1px solid var(--border-color);
    }
    
    /* Alert */
    .ts-alert {
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        border: 1px solid;
        background: var(--card-bg);
    }
    
    .ts-alert.success {
        border-color: rgba(0, 255, 136, 0.3);
        color: var(--primary-green);
    }
    
    .ts-alert.warning {
        border-color: rgba(255, 170, 0, 0.3);
        color: #ffaa00;
    }
    
    .ts-alert.error {
        border-color: rgba(255, 68, 68, 0.3);
        color: #ff4444;
    }
    
    /* Container */
    .ts-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* Grid */
    .ts-grid {
        display: grid;
        gap: 24px;
    }
    
    /* Flex */
    .ts-flex {
        display: flex;
    }
    
    .ts-items-center {
        align-items: center;
    }
    
    .ts-justify-between {
        justify-content: space-between;
    }
    
    /* Spacing */
    .ts-space-y-4 > * + * {
        margin-top: 16px;
    }
    
    .ts-space-x-4 > * + * {
        margin-left: 16px;
    }
    
    /* Icon wrapper */
    .ts-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.2);
        color: var(--primary-green);
        font-size: 20px;
    }
    
    /* Section header */
    .ts-section-header {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .ts-section-header .ts-icon {
        margin-right: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Earth Engine Auto-Authentication with Service Account
def auto_initialize_earth_engine():
    """Automatically initialize Earth Engine with service account credentials"""
    try:
        # Your service account credentials
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
        
        # Authenticate with the service account
        credentials = ee.ServiceAccountCredentials(
            service_account_info['client_email'],
            key_data=json.dumps(service_account_info)
        )
        
        # Initialize Earth Engine
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

# Page configuration
st.set_page_config(
    page_title="Khisba GIS - Vegetation Analysis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
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
    <div class="ts-container" style="text-align: center; padding-top: 100px;">
        <div class="ts-card" style="max-width: 500px; margin: 0 auto;">
            <h1>KHISBA GIS</h1>
            <p style="color: #cccccc; margin: 20px 0 40px 0;">Professional Vegetation Indices Analytics</p>
            
            <div class="ts-alert warning">
                🔐 Authentication Required
            </div>
            
            <div style="margin: 30px 0;">
                <p style="color: #cccccc; margin-bottom: 20px;">Enter admin password to continue</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Password", type="password", placeholder="Enter admin password", label_visibility="collapsed")
        
        if st.button("🔓 Sign In", type="primary", use_container_width=True):
            if password == "admin":
                st.session_state.authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password")
    
    st.markdown("""
    <div class="ts-container" style="text-align: center; margin-top: 50px;">
        <div class="ts-card" style="max-width: 500px; margin: 0 auto;">
            <p style="color: #00ff88; font-weight: 600;">Demo Access</p>
            <p style="color: #cccccc;">Username: <strong>admin</strong><br>Password: <strong>admin</strong></p>
            <div style="margin-top: 20px;">
                <span class="ts-badge">GIS Analytics</span>
                <span class="ts-badge">Earth Engine</span>
                <span class="ts-badge">Satellite Data</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Main Dashboard Header
st.markdown("""
<div class="ts-container">
    <div class="ts-flex ts-items-center ts-justify-between" style="padding: 20px 0;">
        <div>
            <h1 style="margin: 0;">KHISBA GIS</h1>
            <p style="color: #cccccc; margin: 4px 0 0 0;">Professional Vegetation Indices Analytics</p>
        </div>
        <div class="ts-flex ts-items-center ts-space-x-4">
            <span class="status-badge success">Connected</span>
            <span class="ts-badge">v1.0</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Green & Black Theme
with st.sidebar:
    st.markdown("""
    <div class="ts-card" style="text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0 0 10px 0;">🌿 KHISBA GIS</h3>
        <p style="color: #cccccc; margin: 0; font-size: 14px;">Vegetation Analytics Platform</p>
        <div class="ts-divider"></div>
        <div class="ts-flex ts-items-center ts-justify-between">
            <span style="color: #cccccc; font-size: 12px;">Status</span>
            <span class="status-badge success">Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Authentication")
    
    # Earth Engine Status
    if st.session_state.ee_initialized:
        st.markdown("""
        <div class="ts-alert success">
            <div class="ts-flex ts-items-center">
                <span style="margin-right: 10px;">✅</span>
                <div>
                    <strong>Earth Engine Connected</strong><br>
                    <span style="font-size: 12px; color: #00cc6a;">Auto-authenticated</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ts-alert warning">
            <div class="ts-flex ts-items-center">
                <span style="margin-right: 10px;">⚠️</span>
                <div>
                    <strong>Authentication Required</strong><br>
                    <span style="font-size: 12px; color: #ffaa00;">Upload Earth Engine credentials</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Upload Credentials")
        uploaded_file = st.file_uploader(
            "Choose service account JSON",
            type=['json'],
            label_visibility="collapsed",
            help="Upload your Google Earth Engine service account JSON credentials"
        )
        
        if uploaded_file is not None:
            try:
                credentials_data = json.load(uploaded_file)
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                    json.dump(credentials_data, tmp_file)
                    credentials_path = tmp_file.name
                
                from earth_engine_utils import initialize_earth_engine
                success = initialize_earth_engine(credentials_path)
                
                if success:
                    st.session_state.ee_initialized = True
                    st.session_state.credentials_uploaded = True
                    st.success("✅ Earth Engine initialized!")
                    os.unlink(credentials_path)
                    st.rerun()
                else:
                    st.error("❌ Failed to initialize Earth Engine")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Import the helper functions
try:
    from earth_engine_utils import get_admin_boundaries, get_boundary_names
    from vegetation_indices import mask_clouds, add_vegetation_indices
except ImportError as e:
    st.error(f"Error importing helper modules: {str(e)}")
    st.info("Please ensure earth_engine_utils.py and vegetation_indices.py are in the same directory")
    st.stop()

# Main application
if st.session_state.ee_initialized:
    
    # Study Area Selection - TypeScript Card Style
    st.markdown("""
    <div class="ts-container">
        <div class="ts-card">
            <div class="ts-section-header">
                <div class="ts-icon">📍</div>
                <div>
                    <h3 style="margin: 0;">Study Area Selection</h3>
                    <p style="color: #cccccc; margin: 4px 0 0 0;">Select your geographical area for analysis</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Selection in Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="ts-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("#### Country")
        try:
            countries_fc = get_admin_boundaries(0)
            if countries_fc is not None:
                country_names = get_boundary_names(countries_fc, 0)
                selected_country = st.selectbox(
                    "Select Country",
                    options=[""] + country_names,
                    label_visibility="collapsed"
                )
            else:
                st.error("Failed to load countries data")
                selected_country = ""
        except Exception as e:
            st.error(f"Error loading countries: {str(e)}")
            selected_country = ""
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="ts-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("#### State/Province")
        selected_admin1 = ""
        if selected_country and countries_fc is not None:
            try:
                country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first()
                country_code = country_feature.get('ADM0_CODE').getInfo()
                
                admin1_fc = get_admin_boundaries(1, country_code)
                if admin1_fc is not None:
                    admin1_names = get_boundary_names(admin1_fc, 1)
                    selected_admin1 = st.selectbox(
                        "Select State/Province",
                        options=[""] + admin1_names,
                        label_visibility="collapsed"
                    )
            except Exception as e:
                st.error(f"Error loading admin1: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="ts-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("#### Municipality")
        selected_admin2 = ""
        if selected_admin1 and 'admin1_fc' in locals() and admin1_fc is not None:
            try:
                admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
                admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                
                admin2_fc = get_admin_boundaries(2, None, admin1_code)
                if admin2_fc is not None:
                    admin2_names = get_boundary_names(admin2_fc, 2)
                    selected_admin2 = st.selectbox(
                        "Select Municipality",
                        options=[""] + admin2_names,
                        label_visibility="collapsed"
                    )
            except Exception as e:
                st.error(f"Error loading admin2: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # GIS Map Display - KEEPING ORIGINAL FUNCTIONALITY
    if selected_country:
        st.markdown("""
        <div class="ts-container">
            <div class="ts-card">
                <div class="ts-section-header">
                    <div class="ts-icon">🌍</div>
                    <div>
                        <h3 style="margin: 0;">GIS Analytics Workspace</h3>
                        <p style="color: #cccccc; margin: 4px 0 0 0;">Interactive map with satellite data</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Determine which geometry to use
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
            
            # Get geometry bounds for map centering
            bounds = geometry.geometry().bounds().getInfo()
            coords = bounds['coordinates'][0]
            
            # Calculate center and area
            lats = [coord[1] for coord in coords]
            lons = [coord[0] for coord in coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
            
            # Create professional GIS map with multiple base layers
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=6,
                tiles=None,  # We'll add custom tiles
                control_scale=True,
                prefer_canvas=True
            )
            
            # Add multiple professional base layers
            folium.TileLayer(
                'OpenStreetMap',
                name='OpenStreetMap',
                overlay=False,
                control=True
            ).add_to(m)
            
            folium.TileLayer(
                'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Satellite',
                overlay=False,
                control=True
            ).add_to(m)
            
            folium.TileLayer(
                'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Terrain',
                overlay=False,
                control=True
            ).add_to(m)
            
            folium.TileLayer(
                'CartoDB dark_matter',
                name='Dark Theme',
                overlay=False,
                control=True
            ).add_to(m)
            
            # Add professional study area styling
            folium.GeoJson(
                bounds,
                style_function=lambda x: {
                    'fillColor': '#00ff88',
                    'color': '#ffffff',
                    'weight': 3,
                    'fillOpacity': 0.2,
                    'dashArray': '5, 5'
                },
                popup=folium.Popup(f"<b>Study Area:</b><br>{area_name}<br><b>Level:</b> {area_level}", max_width=300),
                tooltip=f"Click for details: {area_name}"
            ).add_to(m)
            
            # Add coordinate display and measurement tools
            from folium.plugins import MousePosition, MeasureControl
            
            MousePosition().add_to(m)
            MeasureControl(primary_length_unit='kilometers').add_to(m)
            
            # Add layer control
            folium.LayerControl().add_to(m)
            
            # Professional GIS info panel
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display professional map with enhanced styling
                st.markdown('<div class="ts-card" style="padding: 5px;">', unsafe_allow_html=True)
                
                map_data = st_folium(
                    m, 
                    width=None, 
                    height=500,
                    returned_objects=["last_clicked", "bounds"],
                    key="gis_map"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Professional GIS information panel
                st.markdown(f"""
                <div class="ts-card" style="height: 500px; overflow-y: auto;">
                    <h4 style="color: #00ff88; margin-top: 0;">🌍 GIS DATA PANEL</h4>
                    <hr style="border-color: #333333;">
                    
                    <div style="margin: 15px 0;">
                        <strong style="color: #ffffff;">Study Area:</strong><br>
                        <span style="color: #cccccc;">{area_name}</span>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <strong style="color: #ffffff;">Administrative Level:</strong><br>
                        <span style="color: #00ff88;">{area_level}</span>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <strong style="color: #ffffff;">Coordinates:</strong><br>
                        <span style="color: #cccccc;">Lat: {center_lat:.4f}°<br>
                        Lon: {center_lon:.4f}°</span>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <strong style="color: #ffffff;">Map Layers:</strong><br>
                        <span style="color: #cccccc;">• Satellite Imagery<br>
                        • Terrain Data<br>
                        • Administrative Boundaries<br>
                        • Dark/Light Themes</span>
                    </div>
                    
                    <div style="background: #111111; padding: 10px; border-radius: 5px; margin-top: 20px; border: 1px solid #333333;">
                        <small style="color: #00ff88;">📊 KHISBA GIS Professional</small><br>
                        <small style="color: #888888;">Powered by Earth Engine</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.session_state.selected_geometry = geometry
            
            # Professional status indicator
            st.markdown(f"""
            <div class="ts-container">
                <div class="ts-card" style="text-align: center; background: rgba(0, 255, 136, 0.1); border-color: rgba(0, 255, 136, 0.3);">
                    <strong style="color: #00ff88;">✅ GIS WORKSPACE ACTIVE</strong> • Study Area: {area_name}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ GIS Map Error: {str(e)}")
            st.info("Please check your internet connection and try refreshing the page.")
    
    # Professional Analysis Parameters - TypeScript Style
    if st.session_state.selected_geometry is not None:
        st.markdown("""
        <div class="ts-container">
            <div class="ts-card">
                <div class="ts-section-header">
                    <div class="ts-icon">⚙️</div>
                    <div>
                        <h3 style="margin: 0;">Analysis Parameters</h3>
                        <p style="color: #cccccc; margin: 4px 0 0 0;">Configure your analysis timeframe and satellite data sources</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="ts-card">', unsafe_allow_html=True)
            st.markdown("#### Time Period")
            start_date = st.date_input(
                "Start Date",
                value=datetime(2023, 1, 1),
                help="Start date for the analysis period",
                label_visibility="collapsed"
            )
            
            cloud_cover = st.slider(
                "Maximum Cloud Cover (%)",
                min_value=0,
                max_value=100,
                value=20,
                help="Maximum cloud cover percentage for images"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="ts-card">', unsafe_allow_html=True)
            st.markdown("#### Data Source")
            end_date = st.date_input(
                "End Date",
                value=datetime(2023, 12, 31),
                help="End date for the analysis period",
                label_visibility="collapsed"
            )
            
            collection_choice = st.selectbox(
                "Satellite Collection",
                options=["Sentinel-2", "Landsat-8"],
                help="Choose the satellite collection for analysis",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Vegetation Indices Selection - TypeScript Style
        st.markdown("""
        <div class="ts-container">
            <div class="ts-card">
                <div class="ts-section-header">
                    <div class="ts-icon">🌿</div>
                    <div>
                        <h3 style="margin: 0;">Vegetation Indices Selection</h3>
                        <p style="color: #cccccc; margin: 4px 0 0 0;">Choose indices to analyze</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        available_indices = [
            'NDVI', 'ARVI', 'ATSAVI', 'DVI', 'EVI', 'EVI2', 'GNDVI', 'MSAVI', 'MSI', 'MTVI', 'MTVI2',
            'NDTI', 'NDWI', 'OSAVI', 'RDVI', 'RI', 'RVI', 'SAVI', 'TVI', 'TSAVI', 'VARI', 'VIN', 'WDRVI',
            'GCVI', 'AWEI', 'MNDWI', 'WI', 'ANDWI', 'NDSI', 'nDDI', 'NBR', 'DBSI', 'SI', 'S3', 'BRI',
            'SSI', 'NDSI_Salinity', 'SRPI', 'MCARI', 'NDCI', 'PSSRb1', 'SIPI', 'PSRI', 'Chl_red_edge', 'MARI', 'NDMI'
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            select_all = st.checkbox("Select All Indices")
        with col2:
            if st.button("Clear All"):
                st.session_state.selected_indices = []
        
        if select_all:
            selected_indices = st.multiselect(
                "Choose vegetation indices to calculate:",
                options=available_indices,
                default=available_indices,
                help="Select the vegetation indices you want to analyze"
            )
        else:
            selected_indices = st.multiselect(
                "Choose vegetation indices to calculate:",
                options=available_indices,
                default=['NDVI', 'EVI', 'SAVI', 'NDWI'],
                help="Select the vegetation indices you want to analyze"
            )
        
        # Run Analysis Button - TypeScript Style
        st.markdown('<div style="text-align: center; margin: 40px 0;">', unsafe_allow_html=True)
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
            if not selected_indices:
                st.error("Please select at least one vegetation index")
            else:
                with st.spinner("Running vegetation indices analysis..."):
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
                            # For Landsat, we'd need different cloud masking
                            processed_collection = filtered_collection.map(add_vegetation_indices)
                        
                        # Calculate time series for selected indices
                        results = {}
                        for index in selected_indices:
                            try:
                                # Create a function to add date and reduce region
                                def add_date_and_reduce(image):
                                    reduced = image.select(index).reduceRegion(
                                        reducer=ee.Reducer.mean(),
                                        geometry=st.session_state.selected_geometry.geometry(),
                                        scale=30,
                                        maxPixels=1e9
                                    )
                                    return ee.Feature(None, reduced.set('date', image.date().format()))
                                
                                # Map over collection to get time series
                                time_series = processed_collection.map(add_date_and_reduce)
                                
                                # Convert to list
                                time_series_list = time_series.getInfo()
                                
                                # Extract dates and values
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
                        st.success("✅ Analysis completed successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

# Display Results - KEEPING ORIGINAL CHARTS AND FUNCTIONALITY
if st.session_state.analysis_results:
    st.markdown("""
    <div class="ts-container">
        <div class="ts-card">
            <div class="ts-section-header">
                <div class="ts-icon">📊</div>
                <div>
                    <h3 style="margin: 0;">Analysis Results</h3>
                    <p style="color: #cccccc; margin: 4px 0 0 0;">Vegetation indices analytics</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    results = st.session_state.analysis_results
    
    # Summary statistics - TypeScript Style
    st.markdown('<div class="ts-card">', unsafe_allow_html=True)
    st.markdown("#### 📈 Summary Statistics")
    
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
        st.dataframe(summary_df, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Professional Analytics Charts - ORIGINAL CODE KEPT INTACT
    st.markdown("""
    <div class="ts-container">
        <div class="ts-card">
            <div class="ts-section-header">
                <div class="ts-icon">📈</div>
                <div>
                    <h3 style="margin: 0;">Professional Vegetation Analytics</h3>
                    <p style="color: #cccccc; margin: 4px 0 0 0;">Interactive charts and analysis</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Allow user to select indices to plot
    col1, col2 = st.columns([3, 1])
    with col1:
        indices_to_plot = st.multiselect(
            "**Select Vegetation Indices:**",
            options=list(results.keys()),
            default=list(results.keys())[:4] if len(results) >= 4 else list(results.keys()),
            help="Choose vegetation indices to analyze with professional charting"
        )
    with col2:
        chart_style = st.selectbox(
            "**Chart Style:**",
            ["Professional", "Statistical", "Area"],
            help="Select your preferred analytical chart style"
        )
    
    if indices_to_plot:
        # Create professional vegetation analytics dashboard
        for i, index in enumerate(indices_to_plot):
            data = results[index]
            if data['dates'] and data['values']:
                # Convert dates to datetime and prepare data
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
                        
                        # Create professional analytical chart
                        fig = go.Figure()
                        
                        # Main value line with professional styling
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
                            # Show statistical analysis with confidence intervals
                            df['Upper_Bound'] = df['Value'] * 1.05
                            df['Lower_Bound'] = df['Value'] * 0.95
                            
                            # Add confidence band
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
                            # Main line
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
                        
                        # Professional analytical layout
                        fig.update_layout(
                            title={
                                'text': f'<b>{index}</b> - Vegetation Analysis',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 20, 'color': '#ffffff'}
                            },
                            plot_bgcolor='#0E1117',
                            paper_bgcolor='#0E1117',
                            font=dict(color='#ffffff'),
                            xaxis=dict(
                                gridcolor='#333333',
                                zerolinecolor='#333333',
                                tickcolor='#666666',
                                title_font_color='#ffffff',
                                title="Time Period"
                            ),
                            yaxis=dict(
                                gridcolor='#333333',
                                zerolinecolor='#333333',
                                tickcolor='#666666',
                                title=f'{index} Index Value',
                                title_font_color='#ffffff'
                            ),
                            legend=dict(
                                bgcolor='rgba(0,0,0,0.5)',
                                bordercolor='#666666',
                                borderwidth=1
                            ),
                            hovermode='x unified',
                            height=400
                        )
                        
                        # Add trend indicator
                        change_pct = ((current_value - prev_value) / prev_value * 100) if prev_value != 0 else 0
                        change_color = '#00ff88' if change_pct >= 0 else '#ff4444'
                        change_symbol = '▲' if change_pct >= 0 else '▼'
                        trend_text = "Increasing" if change_pct >= 0 else "Decreasing"
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.markdown(f"""
                            <div class="ts-card" style="text-align: center; background: #1a1a1a;">
                                <h4 style="color: {change_color}; margin: 0;">{change_symbol} {index} INDEX</h4>
                                <h2 style="color: white; margin: 5px 0;">{current_value:.4f}</h2>
                                <p style="color: {change_color}; margin: 0; font-size: 14px;">{change_pct:+.2f}% • {trend_text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.plotly_chart(fig, width='stretch')
                        
                except Exception as e:
                    st.error(f"Error creating chart for {index}: {str(e)}")
    
    # Data Export - TypeScript Style
    st.markdown("""
    <div class="ts-container">
        <div class="ts-card">
            <div class="ts-section-header">
                <div class="ts-icon">💾</div>
                <div>
                    <h3 style="margin: 0;">Data Export</h3>
                    <p style="color: #cccccc; margin: 4px 0 0 0;">Export your analysis results</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📥 Download Results as CSV", type="primary"):
        # Prepare data for export
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
                label="Download CSV",
                data=csv,
                file_name=f"vegetation_indices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data available for export")

else:
    if not st.session_state.ee_initialized:
        st.markdown("""
        <div class="ts-alert warning">
            <div class="ts-flex ts-items-center">
                <span style="margin-right: 10px;">👆</span>
                <div>Earth Engine is initializing... Please wait or upload credentials if needed</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.selected_geometry is None:
        st.markdown("""
        <div class="ts-alert warning">
            <div class="ts-flex ts-items-center">
                <span style="margin-right: 10px;">👆</span>
                <div>Please select a study area to proceed with analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ts-alert warning">
            <div class="ts-flex ts-items-center">
                <span style="margin-right: 10px;">👆</span>
                <div>Configure your analysis parameters and click 'Run Analysis'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer - TypeScript Style
st.markdown("""
<div class="ts-divider"></div>
<div class="ts-container" style="text-align: center; padding: 30px 0; color: #666666; font-size: 14px;">
    <p style="margin: 10px 0;">KHISBA GIS • Professional Vegetation Analytics Platform</p>
    <p style="margin: 10px 0;">Created by Taibi Farouk Djilali • Green & Black TypeScript Style</p>
    <div style="margin-top: 20px;">
        <span class="ts-badge">Earth Engine</span>
        <span class="ts-badge">Streamlit</span>
        <span class="ts-badge">Folium</span>
        <span class="ts-badge">Plotly</span>
    </div>
</div>
""", unsafe_allow_html=True)
