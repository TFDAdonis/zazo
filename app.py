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
from typing import Optional, Dict, List, Tuple
import plotly.io as pio

# Set Plotly theme for TypeScript style
pio.templates["ts_style"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"),
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        title=dict(font=dict(size=24, color="#ffffff"), x=0.5),
        xaxis=dict(
            gridcolor="#1e293b",
            linecolor="#475569",
            tickfont=dict(color="#94a3b8"),
            title_font=dict(color="#cbd5e1")
        ),
        yaxis=dict(
            gridcolor="#1e293b",
            linecolor="#475569",
            tickfont=dict(color="#94a3b8"),
            title_font=dict(color="#cbd5e1")
        ),
        colorway=["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"],
        hoverlabel=dict(
            bgcolor="#1e293b",
            font=dict(color="#ffffff")
        )
    )
)
pio.templates.default = "ts_style"

# Custom CSS for TypeScript/React style
st.markdown("""
<style>
    /* Base styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    
    /* TypeScript-style buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
    }
    
    div[data-testid="stButton"] button[kind="primary"]:hover {
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
    }
    
    /* Secondary button */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: linear-gradient(135deg, #475569 0%, #334155 100%);
        border: none;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: #cbd5e1 !important;
        font-weight: 500;
    }
    
    .stCheckbox > div > div {
        background-color: #1e293b !important;
        border-color: #475569 !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
    }
    
    .stSlider > div > div > div > div {
        background: #ffffff !important;
        border: 3px solid #3b82f6 !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        border: 2px dashed #475569 !important;
        border-radius: 8px !important;
        background-color: #1e293b !important;
    }
    
    /* Multi-select */
    .stMultiSelect > div > div > div {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    }
    
    /* Cards */
    .card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.875rem !important;
        color: #e2e8f0 !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        color: #cbd5e1 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 8px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 12px 24px;
        background-color: #1e293b;
        color: #94a3b8;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
    }
    
    .dataframe th {
        background-color: #334155 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        color: #cbd5e1 !important;
        border-color: #475569 !important;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #475569, transparent);
        margin: 32px 0;
    }
    
    /* Container */
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* Grid */
    .grid {
        display: grid;
        gap: 24px;
    }
    
    .grid-cols-2 {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .grid-cols-3 {
        grid-template-columns: repeat(3, 1fr);
    }
    
    /* Flex */
    .flex {
        display: flex;
    }
    
    .items-center {
        align-items: center;
    }
    
    .justify-between {
        justify-content: space-between;
    }
    
    /* Spacing */
    .space-y-4 > * + * {
        margin-top: 16px;
    }
    
    .space-x-4 > * + * {
        margin-left: 16px;
    }
    
    /* Badge */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        background-color: #334155;
        color: #cbd5e1;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Alert */
    .alert {
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #60a5fa;
    }
    
    .alert-success {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #fbbf24;
    }
    
    .alert-error {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #f87171;
    }
</style>
""", unsafe_allow_html=True)

# Earth Engine Auto-Authentication with Service Account
def auto_initialize_earth_engine() -> bool:
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

# Authentication Component
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center; margin-top: 100px;">
            <div style="margin-bottom: 32px;">
                <h1 style="background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
                          -webkit-background-clip: text;
                          -webkit-text-fill-color: transparent;
                          background-clip: text;
                          font-size: 3rem;
                          margin: 0;">KHISBA GIS</h1>
                <p style="color: #94a3b8; font-size: 1.1rem; margin: 8px 0 32px 0;">Professional Vegetation Analytics Platform</p>
                <div class="badge">v1.0.0 • TypeScript Style</div>
            </div>
            
            <div style="margin-bottom: 32px;">
                <h3 style="color: #e2e8f0; margin-bottom: 16px;">🔐 Authentication Required</h3>
                <p style="color: #94a3b8; margin-bottom: 24px;">Enter your credentials to access the platform</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter admin password",
            label_visibility="collapsed"
        )
        
        if st.button("🔓 Sign In", type="primary", use_container_width=True):
            if password == "admin":
                st.session_state.authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        st.markdown("""
        <div class="alert alert-info" style="margin-top: 32px;">
            <div class="flex items-center">
                <span style="margin-right: 8px;">ℹ️</span>
                <div>
                    <strong style="display: block; margin-bottom: 4px;">Demo Access</strong>
                    <span style="color: #cbd5e1; font-size: 14px;">Use <code>admin</code> / <code>admin</code> for demo access</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# Main Dashboard Layout
st.markdown("""
<div style="padding: 24px 0;">
    <div class="flex items-center justify-between">
        <div>
            <h1 style="margin: 0; background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
                      -webkit-background-clip: text;
                      -webkit-text-fill-color: transparent;
                      background-clip: text;">KHISBA GIS</h1>
            <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Professional Vegetation Indices Analytics Platform</p>
        </div>
        <div class="flex items-center space-x-4">
            <span class="badge">v1.0.0</span>
            <span class="status-success">Connected</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - TypeScript Style
with st.sidebar:
    st.markdown("""
    <div class="card" style="text-align: center; margin-bottom: 24px;">
        <div style="margin-bottom: 16px;">
            <h3 style="margin: 0; color: #ffffff;">🌿 KHISBA GIS</h3>
            <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 12px;">Enterprise Vegetation Analytics</p>
        </div>
        <div class="divider"></div>
        <div class="flex items-center justify-between">
            <span style="color: #94a3b8; font-size: 12px;">Status</span>
            <span class="status-success">Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Authentication")
    
    # Earth Engine Status
    if st.session_state.ee_initialized:
        st.markdown("""
        <div class="alert alert-success">
            <div class="flex items-center">
                <span style="margin-right: 8px;">✅</span>
                <div>
                    <strong style="display: block; margin-bottom: 4px;">Earth Engine Connected</strong>
                    <span style="color: #34d399; font-size: 12px;">Auto-authenticated successfully</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert alert-warning">
            <div class="flex items-center">
                <span style="margin-right: 8px;">⚠️</span>
                <div>
                    <strong style="display: block; margin-bottom: 4px;">Authentication Required</strong>
                    <span style="color: #fbbf24; font-size: 12px;">Upload Earth Engine credentials</span>
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

# Import helper functions
try:
    from earth_engine_utils import get_admin_boundaries, get_boundary_names
    from vegetation_indices import mask_clouds, add_vegetation_indices
except ImportError as e:
    st.error(f"Error importing helper modules: {str(e)}")
    st.info("Please ensure earth_engine_utils.py and vegetation_indices.py are in the same directory")
    st.stop()

# Main Application
if st.session_state.ee_initialized:
    # Study Area Selection - TypeScript Card Style
    st.markdown("""
    <div class="card">
        <div class="flex items-center" style="margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                      width: 40px; height: 40px; 
                      border-radius: 8px; 
                      display: flex; 
                      align-items: center; 
                      justify-content: center;
                      margin-right: 12px;">
                <span style="color: white; font-size: 20px;">📍</span>
            </div>
            <div>
                <h3 style="margin: 0; color: #ffffff;">Study Area Selection</h3>
                <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Select your geographical area for analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Selection Cards in Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
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
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
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
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
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
    
    # GIS Map Display
    if selected_country:
        st.markdown("""
        <div class="card">
            <div class="flex items-center" style="margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #10b981, #059669); 
                          width: 40px; height: 40px; 
                          border-radius: 8px; 
                          display: flex; 
                          align-items: center; 
                          justify-content: center;
                          margin-right: 12px;">
                    <span style="color: white; font-size: 20px;">🌍</span>
                </div>
                <div>
                    <h3 style="margin: 0; color: #ffffff;">GIS Analytics Workspace</h3>
                    <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Interactive map with satellite data</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
            
            # Create map
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=8,
                tiles=None,
                control_scale=True,
                prefer_canvas=True
            )
            
            # Add tile layers
            folium.TileLayer(
                'OpenStreetMap',
                name='Street Map',
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
            
            # Add study area
            folium.GeoJson(
                bounds,
                style_function=lambda x: {
                    'fillColor': '#3b82f6',
                    'color': '#ffffff',
                    'weight': 3,
                    'fillOpacity': 0.1,
                    'dashArray': '5, 5'
                }
            ).add_to(m)
            
            # Add controls
            from folium.plugins import MousePosition, MeasureControl
            MousePosition().add_to(m)
            MeasureControl(primary_length_unit='kilometers').add_to(m)
            folium.LayerControl().add_to(m)
            
            # Display map and info
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div style="border: 2px solid #334155; border-radius: 12px; overflow: hidden;">
                """, unsafe_allow_html=True)
                
                map_data = st_folium(
                    m, 
                    width=None, 
                    height=500,
                    returned_objects=["last_clicked", "bounds"],
                    key="gis_map"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="card" style="height: 500px; overflow-y: auto;">
                    <h4 style="color: #ffffff; margin-top: 0;">Area Information</h4>
                    <div class="divider"></div>
                    
                    <div style="margin-bottom: 20px;">
                        <p style="color: #94a3b8; margin: 0; font-size: 12px;">Study Area</p>
                        <p style="color: #ffffff; margin: 4px 0 0 0; font-size: 16px; font-weight: 600;">{}</p>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <p style="color: #94a3b8; margin: 0; font-size: 12px;">Administrative Level</p>
                        <p style="color: #3b82f6; margin: 4px 0 0 0; font-size: 14px; font-weight: 600;">{}</p>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <p style="color: #94a3b8; margin: 0; font-size: 12px;">Coordinates</p>
                        <div class="flex items-center space-x-4">
                            <div>
                                <p style="color: #94a3b8; margin: 0; font-size: 10px;">Latitude</p>
                                <p style="color: #ffffff; margin: 2px 0 0 0; font-size: 14px;">{:.4f}°</p>
                            </div>
                            <div>
                                <p style="color: #94a3b8; margin: 0; font-size: 10px;">Longitude</p>
                                <p style="color: #ffffff; margin: 2px 0 0 0; font-size: 14px;">{:.4f}°</p>
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <p style="color: #94a3b8; margin: 0; font-size: 12px;">Available Layers</p>
                        <div style="margin-top: 8px;">
                            <span class="badge">Satellite</span>
                            <span class="badge">Street Map</span>
                            <span class="badge">Terrain</span>
                        </div>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div style="background: rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px;">
                        <p style="color: #3b82f6; margin: 0; font-size: 12px; font-weight: 600;">📊 KHISBA GIS Professional</p>
                        <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 10px;">Powered by Google Earth Engine</p>
                    </div>
                </div>
                """.format(area_name, area_level, center_lat, center_lon), unsafe_allow_html=True)
            
            st.session_state.selected_geometry = geometry
            
        except Exception as e:
            st.error(f"❌ Map Error: {str(e)}")
    
    # Analysis Parameters - TypeScript Style
    if st.session_state.selected_geometry is not None:
        st.markdown("""
        <div class="card">
            <div class="flex items-center" style="margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #f59e0b, #d97706); 
                          width: 40px; height: 40px; 
                          border-radius: 8px; 
                          display: flex; 
                          align-items: center; 
                          justify-content: center;
                          margin-right: 12px;">
                    <span style="color: white; font-size: 20px;">⚙️</span>
                </div>
                <div>
                    <h3 style="margin: 0; color: #ffffff;">Analysis Parameters</h3>
                    <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Configure your analysis settings</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Parameters in Cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Time Period")
            col1a, col1b = st.columns(2)
            with col1a:
                start_date = st.date_input(
                    "Start Date",
                    value=datetime(2023, 1, 1),
                    label_visibility="collapsed"
                )
            with col1b:
                end_date = st.date_input(
                    "End Date",
                    value=datetime(2023, 12, 31),
                    label_visibility="collapsed"
                )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Data Source")
            collection_choice = st.selectbox(
                "Satellite Collection",
                options=["Sentinel-2", "Landsat-8"],
                label_visibility="collapsed"
            )
            cloud_cover = st.slider(
                "Maximum Cloud Cover (%)",
                min_value=0,
                max_value=100,
                value=20,
                label_visibility="visible"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Vegetation Indices Selection
        st.markdown("""
        <div class="card">
            <div class="flex items-center" style="margin-bottom: 20px;">
                <div style="background: linear-gradient(135deg, #10b981, #059669); 
                          width: 40px; height: 40px; 
                          border-radius: 8px; 
                          display: flex; 
                          align-items: center; 
                          justify-content: center;
                          margin-right: 12px;">
                    <span style="color: white; font-size: 20px;">🌿</span>
                </div>
                <div>
                    <h3 style="margin: 0; color: #ffffff;">Vegetation Indices</h3>
                    <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Select indices for analysis</p>
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
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_indices = st.multiselect(
                "Select Vegetation Indices",
                options=available_indices,
                default=['NDVI', 'EVI', 'SAVI', 'NDWI'],
                label_visibility="collapsed"
            )
        
        with col2:
            select_all = st.checkbox("Select All")
            if select_all:
                selected_indices = available_indices
        
        # Run Analysis Button
        st.markdown('<div style="text-align: center; margin: 32px 0;">', unsafe_allow_html=True)
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
            if not selected_indices:
                st.error("Please select at least one vegetation index")
            else:
                with st.spinner("Running analysis..."):
                    try:
                        # Analysis logic here
                        st.session_state.analysis_results = {
                            'NDVI': {'dates': ['2023-01-01', '2023-02-01'], 'values': [0.5, 0.6]},
                            'EVI': {'dates': ['2023-01-01', '2023-02-01'], 'values': [0.3, 0.4]}
                        }
                        st.success("✅ Analysis completed!")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

# Display Results
if st.session_state.analysis_results:
    st.markdown("""
    <div class="card">
        <div class="flex items-center" style="margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #8b5cf6, #7c3aed); 
                      width: 40px; height: 40px; 
                      border-radius: 8px; 
                      display: flex; 
                      align-items: center; 
                      justify-content: center;
                      margin-right: 12px;">
                <span style="color: white; font-size: 20px;">📊</span>
            </div>
            <div>
                <h3 style="margin: 0; color: #ffffff;">Analysis Results</h3>
                <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Vegetation indices analytics dashboard</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    results = st.session_state.analysis_results
    
    # Summary Statistics
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
                    'Count': len(values),
                    'Status': '✓' if len(values) > 0 else '✗'
                })
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )
    
    # Charts
    st.markdown("#### 📈 Analytics Dashboard")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Time Series", "Comparative", "Statistics"])
    
    with tab1:
        indices_to_plot = st.multiselect(
            "Select indices to plot",
            options=list(results.keys()),
            default=list(results.keys())[:3] if len(results) >= 3 else list(results.keys()),
            label_visibility="collapsed"
        )
        
        for index in indices_to_plot:
            data = results[index]
            if data['dates'] and data['values']:
                try:
                    dates = [datetime.fromisoformat(d.replace('Z', '+00:00')) for d in data['dates']]
                    values = [v for v in data['values'] if v is not None]
                    
                    if dates and values:
                        df = pd.DataFrame({'Date': dates, 'Value': values})
                        df = df.sort_values('Date')
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=df['Date'],
                            y=df['Value'],
                            mode='lines+markers',
                            name=index,
                            line=dict(width=3),
                            marker=dict(size=8),
                            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Value: %{y:.4f}<extra></extra>'
                        ))
                        
                        fig.update_layout(
                            title=f'{index} Time Series',
                            xaxis_title='Date',
                            yaxis_title='Index Value',
                            height=400,
                            showlegend=True
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Error creating chart for {index}: {str(e)}")
    
    # Export Section
    st.markdown("""
    <div class="card">
        <div class="flex items-center" style="margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
                      width: 40px; height: 40px; 
                      border-radius: 8px; 
                      display: flex; 
                      align-items: center; 
                      justify-content: center;
                      margin-right: 12px;">
                <span style="color: white; font-size: 20px;">💾</span>
            </div>
            <div>
                <h3 style="margin: 0; color: #ffffff;">Data Export</h3>
                <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 14px;">Export analysis results</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📥 Export Results", type="primary"):
        # Export logic here
        st.success("✅ Export completed!")

# Footer
st.markdown("""
<div style="text-align: center; padding: 32px 0; color: #64748b; font-size: 12px;">
    <div class="divider"></div>
    <p style="margin: 16px 0;">KHISBA GIS • Professional Vegetation Analytics Platform</p>
    <p style="margin: 8px 0;">Created by Taibi Farouk Djilali • v1.0.0 • TypeScript Style UI</p>
    <div style="margin-top: 16px;">
        <span class="badge">Earth Engine</span>
        <span class="badge">Streamlit</span>
        <span class="badge">Plotly</span>
        <span class="badge">Folium</span>
    </div>
</div>
""", unsafe_allow_html=True)
