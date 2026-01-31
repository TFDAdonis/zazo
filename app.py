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

# Custom CSS for Exact Replit Design Match
st.markdown("""
<style>
    /* Base styling */
    .stApp {
        background: #0d1117 !important;
        color: #c9d1d9 !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Remove all Streamlit default styling */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Dark theme colors */
    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --border-color: #30363d;
        --text-primary: #c9d1d9;
        --text-secondary: #8b949e;
        --text-accent: #58a6ff;
        --green-accent: #2ea043;
        --button-bg: #238636;
        --button-hover: #2ea043;
    }
    
    /* Main layout containers */
    .app-container {
        display: flex;
        min-height: 100vh;
        background: var(--bg-primary);
    }
    
    .left-panel {
        width: 380px;
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
        padding: 20px;
        overflow-y: auto;
    }
    
    .right-panel {
        flex: 1;
        padding: 20px;
        background: var(--bg-primary);
    }
    
    /* Typography - exact match */
    h1 {
        color: var(--text-primary) !important;
        font-size: 24px !important;
        font-weight: 600 !important;
        margin: 0 0 8px 0 !important;
        padding: 0 !important;
    }
    
    h2 {
        color: var(--text-primary) !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin: 24px 0 16px 0 !important;
        padding: 0 !important;
    }
    
    h3 {
        color: var(--text-primary) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin: 0 0 12px 0 !important;
        padding: 0 !important;
    }
    
    p, .text-muted {
        color: var(--text-secondary) !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        margin: 8px 0 !important;
    }
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: 24px !important;
    }
    
    /* Form elements - exact match */
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-label {
        display: block;
        color: var(--text-primary);
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .form-input {
        width: 100%;
        padding: 8px 12px;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        color: var(--text-primary);
        font-size: 14px;
        transition: border-color 0.2s;
    }
    
    .form-input:focus {
        outline: none;
        border-color: var(--text-accent);
        box-shadow: 0 0 0 3px rgba(56, 139, 253, 0.15);
    }
    
    /* Checkbox */
    .checkbox-group {
        display: flex;
        align-items: center;
        margin: 16px 0;
    }
    
    .checkbox-label {
        color: var(--text-primary);
        font-size: 14px;
        margin-left: 8px;
    }
    
    /* Button - exact match */
    .primary-button {
        width: 100%;
        padding: 12px;
        background: var(--button-bg);
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s;
        margin: 16px 0;
    }
    
    .primary-button:hover {
        background: var(--button-hover);
    }
    
    /* Map container - exact match */
    .map-container {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 20px;
        margin: 20px 0;
        min-height: 400px;
        position: relative;
    }
    
    .map-placeholder {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: var(--text-secondary);
    }
    
    /* Map controls */
    .map-controls {
        display: flex;
        gap: 8px;
        margin-top: 16px;
    }
    
    .control-button {
        padding: 6px 12px;
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        color: var(--text-primary);
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .control-button:hover {
        background: var(--bg-tertiary);
        border-color: var(--text-accent);
    }
    
    /* Status indicators */
    .status-tag {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        background: rgba(46, 160, 67, 0.1);
        border: 1px solid rgba(46, 160, 67, 0.2);
        border-radius: 12px;
        color: var(--green-accent);
        font-size: 12px;
        margin: 4px;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: var(--border-color);
        margin: 24px 0;
    }
    
    /* Info panel below map */
    .map-info {
        display: flex;
        gap: 16px;
        margin-top: 16px;
        font-size: 13px;
        color: var(--text-secondary);
    }
    
    /* Footer */
    .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid var(--border-color);
        text-align: center;
        color: var(--text-secondary);
        font-size: 13px;
    }
    
    .footer-button {
        display: inline-block;
        margin: 16px auto;
        padding: 8px 20px;
        background: var(--button-bg);
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none;
    }
    
    .footer-note {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 8px;
    }
    
    /* Override Streamlit components */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
    }
    
    .stSlider > div > div > div {
        background: var(--green-accent) !important;
    }
    
    .stSlider > div > div > div > div {
        background: white !important;
        border: 2px solid var(--green-accent) !important;
    }
    
    .stCheckbox > label {
        color: var(--text-primary) !important;
        font-size: 14px !important;
    }
    
    /* Hide Streamlit labels */
    .stSelectbox label,
    .stSlider label,
    .stDateInput label {
        visibility: hidden;
        height: 0;
        margin: 0;
        padding: 0;
    }
    
    /* Custom select styling */
    .custom-select {
        position: relative;
    }
    
    .custom-select select {
        appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%238b949e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 12px center;
        padding-right: 36px !important;
    }
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
        return False

# Initialize Earth Engine
if 'ee_initialized' not in st.session_state:
    with st.spinner("Initializing..."):
        if auto_initialize_earth_engine():
            st.session_state.ee_initialized = True
        else:
            st.session_state.ee_initialized = False

# Page configuration
st.set_page_config(
    page_title="KHISBA GIS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True  # Auto-authenticate for demo
if 'selected_geometry' not in st.session_state:
    st.session_state.selected_geometry = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Auto-authenticate for this design
st.session_state.authenticated = True

if not st.session_state.authenticated:
    st.stop()

# Main App Layout
st.markdown("""
<div class="app-container">
    <div class="left-panel">
        <h1>KHISBA GIS</h1>
        <p class="subtitle">Vegetation Analytics</p>
        <p class="text-muted">Pick an area, choose an index, then run.</p>
        
        <div class="divider"></div>
        
        <h2>Quick setup</h2>
        
        <div class="form-group">
            <div class="form-label">Area name</div>
            <div class="custom-select">
""", unsafe_allow_html=True)

# Area selection
try:
    from earth_engine_utils import get_admin_boundaries, get_boundary_names
except:
    pass

# Show area name input
area_name = st.text_input("", value="KHISBA_Test_AOL01", label_visibility="collapsed", key="area_name")

st.markdown("""
            </div>
            <p class="text-muted" style="font-size: 13px; margin-top: 8px;">Use Draw/Upload in the map panel (placeholder).</p>
        </div>
        
        <div class="form-group">
            <div class="form-label">Vegetation index</div>
            <div class="custom-select">
""", unsafe_allow_html=True)

# Vegetation index selection
index_options = ['NDVI', 'EVI', 'SAVI', 'NDWI', 'MSAVI', 'GNDVI', 'ARVI', 'VARI']
selected_index = st.selectbox("", options=index_options, index=0, label_visibility="collapsed", key="veg_index")

st.markdown(f"""
            </div>
            <p class="text-muted" style="font-size: 13px; margin-top: 8px;">{selected_index} - Vegetation vigor</p>
        </div>
        
        <div class="checkbox-group">
            <input type="checkbox" id="run_analysis" name="run_analysis" checked>
            <label for="run_analysis" class="checkbox-label">Run analysis</label>
        </div>
        
        <p class="text-muted" style="font-size: 13px;">Analysis is simulated for the mockup.</p>
        
        <div class="divider"></div>
        
        <h2>More options</h2>
        
        <div class="form-group">
            <div class="form-label">Cloud max</div>
""", unsafe_allow_html=True)

# Cloud cover slider
cloud_cover = st.slider("", 0, 100, 28, label_visibility="collapsed", key="cloud_slider")

st.markdown(f"""
            <p class="text-muted" style="font-size: 13px; margin-top: 8px;">{cloud_cover}%</p>
        </div>
        
        <div class="checkbox-group">
            <input type="checkbox" id="apply_mask" name="apply_mask" checked>
            <label for="apply_mask" class="checkbox-label">Apply mask</label>
        </div>
        
        <p class="text-muted" style="font-size: 13px;">Reduce false positives.</p>
        
        <div class="divider"></div>
        
        <button class="primary-button" onclick="runAnalysis()">Run Analysis</button>
        
        <div class="footer">
            <button class="footer-button">Activate VV Made With Replit</button>
            <p class="footer-note">Use the left panel, then run analytics vs.</p>
        </div>
    </div>
    
    <div class="right-panel">
        <h2 style="margin-top: 0;">Map</h2>
        <p class="text-muted">Draw / Upload area (visual placeholder)</p>
        
        <div class="map-container">
            <div class="map-placeholder">
                <div style="font-size: 48px; margin-bottom: 16px;">🗺️</div>
                <h3 style="margin-bottom: 8px;">Interactive Map Area</h3>
                <p style="max-width: 300px; margin: 0 auto;">Click "Draw" to define your analysis area or upload a GeoJSON file</p>
            </div>
        </div>
        
        <div class="map-info">
            <span class="status-tag">NDVI</span>
            <span class="status-tag">cloud ≤ {cloud_cover}%</span>
            <span class="status-tag">mask: on</span>
            <span class="status-tag">smooth: on</span>
        </div>
        
        <div class="divider"></div>
        
        <h3>Basemap</h3>
        <div class="map-controls">
            <button class="control-button">Basemap</button>
            <button class="control-button">Layers</button>
            <button class="control-button">Draw</button>
            <button class="control-button">Upload</button>
            <button class="control-button">Center</button>
        </div>
    </div>
</div>

<script>
function runAnalysis() {
    alert("Analysis started! This is a mockup demonstration.");
}
</script>
""", unsafe_allow_html=True)

# Add JavaScript for interactive elements
st.markdown("""
<script>
// Add interactivity to checkboxes
document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        console.log(this.id + ' changed to ' + this.checked);
    });
});

// Add interactivity to control buttons
document.querySelectorAll('.control-button').forEach(button => {
    button.addEventListener('click', function() {
        const action = this.textContent;
        if (action === 'Draw') {
            alert('Draw mode activated. Click on the map to start drawing.');
        } else if (action === 'Upload') {
            alert('Upload dialog would open here.');
        } else if (action === 'Center') {
            alert('Map centered to selected area.');
        } else {
            alert(action + ' options would appear here.');
        }
    });
});

// Add interactivity to footer button
document.querySelector('.footer-button').addEventListener('click', function() {
    alert('Activating VV Made With Replit feature...');
});
</script>
""", unsafe_allow_html=True)

# Hidden Streamlit functionality that runs in background
if st.session_state.ee_initialized:
    st.markdown("""
    <script>
    console.log('Earth Engine initialized successfully');
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
    console.log('Earth Engine not initialized - using mock data');
    </script>
    """, unsafe_allow_html=True)

# Simulate analysis when Run Analysis is clicked
if st.button(" ", key="hidden_run", help="Run analysis"):
    st.session_state.analysis_results = {
        'NDVI': {'dates': ['2024-01-01', '2024-02-01', '2024-03-01'], 'values': [0.45, 0.52, 0.48]},
        'status': 'Analysis complete - mock data generated'
    }
    
    st.markdown("""
    <script>
    alert('Analysis complete! Results generated with mock data.');
    </script>
    """, unsafe_allow_html=True)

# Add some interactivity with session state
if 'analysis_triggered' not in st.session_state:
    st.session_state.analysis_triggered = False

# Store the selected values
st.session_state.selected_area = area_name
st.session_state.selected_index = selected_index
st.session_state.cloud_max = cloud_cover
