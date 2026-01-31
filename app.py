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
    .stToolbar {display: none;}
    
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
        --slider-track: #238636;
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
        flex-shrink: 0;
    }
    
    .right-panel {
        flex: 1;
        padding: 20px;
        background: var(--bg-primary);
        min-width: 0;
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
        box-sizing: border-box;
    }
    
    .form-input:focus {
        outline: none;
        border-color: var(--text-accent);
        box-shadow: 0 0 0 3px rgba(56, 139, 253, 0.15);
    }
    
    /* Checkbox styling */
    .checkbox-container {
        display: flex;
        align-items: center;
        margin: 16px 0;
        cursor: pointer;
    }
    
    .checkbox-input {
        margin: 0;
        margin-right: 8px;
        width: 16px;
        height: 16px;
        cursor: pointer;
    }
    
    .checkbox-label {
        color: var(--text-primary);
        font-size: 14px;
        cursor: pointer;
        user-select: none;
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
        padding: 40px 20px;
        margin: 20px 0;
        min-height: 400px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .map-placeholder {
        text-align: center;
        color: var(--text-secondary);
    }
    
    .map-placeholder-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.5;
    }
    
    /* Map controls */
    .map-controls {
        display: flex;
        gap: 8px;
        margin-top: 16px;
        flex-wrap: wrap;
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
        white-space: nowrap;
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
        margin: 4px 4px 4px 0;
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
        flex-wrap: wrap;
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
        transition: background-color 0.2s;
    }
    
    .footer-button:hover {
        background: var(--button-hover);
    }
    
    .footer-note {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 8px;
    }
    
    /* Custom select styling */
    .custom-select-container {
        position: relative;
    }
    
    .custom-select-container::after {
        content: "▼";
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-secondary);
        font-size: 10px;
        pointer-events: none;
    }
    
    /* Override Streamlit components */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextInput > div > div {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        box-sizing: border-box !important;
        min-height: 38px !important;
    }
    
    .stSelectbox > div > div > select {
        appearance: none !important;
        padding-right: 30px !important;
    }
    
    /* Slider styling */
    .stSlider > div > div {
        padding: 8px 0 !important;
    }
    
    .stSlider > div > div > div {
        background: var(--slider-track) !important;
        height: 6px !important;
        border-radius: 3px !important;
    }
    
    .stSlider > div > div > div > div {
        background: white !important;
        border: 2px solid var(--green-accent) !important;
        width: 16px !important;
        height: 16px !important;
    }
    
    .stSlider > div > div > div > div > div {
        background: var(--green-accent) !important;
    }
    
    /* Hide Streamlit labels and help text */
    .stSelectbox > label,
    .stSlider > label,
    .stTextInput > label,
    .stDateInput > label,
    .stTextInput > div > p,
    .stSelectbox > div > p {
        display: none !important;
    }
    
    /* Remove Streamlit spacing */
    div[data-testid="stHorizontalBlock"] > div {
        padding: 0 !important;
    }
    
    /* Custom radio buttons */
    .stRadio > div {
        flex-direction: row !important;
        gap: 16px !important;
    }
    
    .stRadio > div > label {
        color: var(--text-primary) !important;
        font-size: 14px !important;
    }
    
    /* Make sure columns work properly */
    .stColumn {
        padding: 0 !important;
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
if 'run_analysis_checked' not in st.session_state:
    st.session_state.run_analysis_checked = True
if 'apply_mask_checked' not in st.session_state:
    st.session_state.apply_mask_checked = True

# Main App Layout
st.markdown("""
<div class="app-container">
    <div class="left-panel">
""", unsafe_allow_html=True)

# Left Panel Content
st.markdown("<h1>KHISBA GIS</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Vegetation Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="text-muted">Pick an area, choose an index, then run.</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

st.markdown("<h2>Quick setup</h2>", unsafe_allow_html=True)

# Area name input
st.markdown('<div class="form-group">', unsafe_allow_html=True)
st.markdown('<div class="form-label">Area name</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-select-container">', unsafe_allow_html=True)

area_name = st.text_input(
    "",
    value="KHISBA_Test_AOL01",
    label_visibility="collapsed",
    key="area_name_input"
)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<p class="text-muted" style="font-size: 13px; margin-top: 8px;">Use Draw/Upload in the map panel (placeholder).</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Vegetation index selection
st.markdown('<div class="form-group">', unsafe_allow_html=True)
st.markdown('<div class="form-label">Vegetation index</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-select-container">', unsafe_allow_html=True)

index_options = ['NDVI', 'EVI', 'SAVI', 'NDWI', 'MSAVI', 'GNDVI', 'ARVI', 'VARI']
selected_index = st.selectbox(
    "",
    options=index_options,
    index=0,
    label_visibility="collapsed",
    key="veg_index_select"
)

st.markdown('</div>', unsafe_allow_html=True)

# Get index description
index_descriptions = {
    'NDVI': 'Normalized Difference Vegetation Index - Vegetation vigor',
    'EVI': 'Enhanced Vegetation Index - Improved vegetation monitoring',
    'SAVI': 'Soil Adjusted Vegetation Index - Accounts for soil brightness',
    'NDWI': 'Normalized Difference Water Index - Water content detection',
    'MSAVI': 'Modified Soil Adjusted Vegetation Index - Enhanced soil adjustment',
    'GNDVI': 'Green Normalized Difference Vegetation Index - Chlorophyll content',
    'ARVI': 'Atmospherically Resistant Vegetation Index - Reduces atmospheric effects',
    'VARI': 'Visible Atmospherically Resistant Index - Visible spectrum vegetation'
}

index_desc = index_descriptions.get(selected_index, 'Vegetation vigor')
st.markdown(f'<p class="text-muted" style="font-size: 13px; margin-top: 8px;">{index_desc}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Run analysis checkbox
st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
run_analysis = st.checkbox(
    "Run analysis",
    value=st.session_state.run_analysis_checked,
    key="run_analysis_checkbox",
    label_visibility="collapsed"
)
st.markdown('<label for="run_analysis_checkbox" class="checkbox-label">Run analysis</label>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="text-muted" style="font-size: 13px;">Analysis is simulated for the mockup.</p>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("<h2>More options</h2>", unsafe_allow_html=True)

# Cloud max slider
st.markdown('<div class="form-group">', unsafe_allow_html=True)
st.markdown('<div class="form-label">Cloud max</div>', unsafe_allow_html=True)

cloud_cover = st.slider(
    "",
    0, 100, 28,
    label_visibility="collapsed",
    key="cloud_slider_input"
)

st.markdown(f'<p class="text-muted" style="font-size: 13px; margin-top: 8px;">{cloud_cover}%</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Apply mask checkbox
st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
apply_mask = st.checkbox(
    "Apply mask",
    value=st.session_state.apply_mask_checked,
    key="apply_mask_checkbox",
    label_visibility="collapsed"
)
st.markdown('<label for="apply_mask_checkbox" class="checkbox-label">Apply mask</label>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="text-muted" style="font-size: 13px;">Reduce false positives.</p>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Run Analysis Button
if st.button("Run Analysis", key="run_analysis_button"):
    st.session_state.analysis_triggered = True
    st.markdown("""
    <script>
    alert('Analysis started! This is a mockup demonstration.');
    </script>
    """, unsafe_allow_html=True)

st.markdown("""
        <div class="footer">
            <button class="footer-button" onclick="activateVV()">Activate VV Made With Replit</button>
            <p class="footer-note">Use the left panel, then run analytics vs.</p>
        </div>
    </div>
    
    <div class="right-panel">
        <h2 style="margin-top: 0;">Map</h2>
        <p class="text-muted">Draw / Upload area (visual placeholder)</p>
        
        <div class="map-container">
            <div class="map-placeholder">
                <div class="map-placeholder-icon">🗺️</div>
                <h3 style="margin-bottom: 8px;">Interactive Map Area</h3>
                <p style="max-width: 300px; margin: 0 auto;">Click "Draw" to define your analysis area or upload a GeoJSON file</p>
            </div>
        </div>
        
        <div class="map-info">
""", unsafe_allow_html=True)

# Status tags
st.markdown(f'<span class="status-tag">{selected_index}</span>', unsafe_allow_html=True)
st.markdown(f'<span class="status-tag">cloud ≤ {cloud_cover}%</span>', unsafe_allow_html=True)
st.markdown('<span class="status-tag">mask: on</span>', unsafe_allow_html=True)
st.markdown('<span class="status-tag">smooth: on</span>', unsafe_allow_html=True)

st.markdown("""
        </div>
        
        <div class="divider"></div>
        
        <h3>Basemap</h3>
        <div class="map-controls">
            <button class="control-button" onclick="showBasemap()">Basemap</button>
            <button class="control-button" onclick="showLayers()">Layers</button>
            <button class="control-button" onclick="startDrawing()">Draw</button>
            <button class="control-button" onclick="uploadFile()">Upload</button>
            <button class="control-button" onclick="centerMap()">Center</button>
        </div>
    </div>
</div>

<script>
function activateVV() {
    alert('Activating VV Made With Replit feature...');
}

function showBasemap() {
    alert('Basemap options would appear here.');
}

function showLayers() {
    alert('Layer management panel would open.');
}

function startDrawing() {
    alert('Draw mode activated. Click on the map to start drawing your area.');
}

function uploadFile() {
    alert('File upload dialog would open here. Supported formats: GeoJSON, KML, Shapefile.');
}

function centerMap() {
    alert('Map centered to selected area.');
}
</script>
""", unsafe_allow_html=True)

# Add JavaScript for better interactivity
st.markdown("""
<script>
// Update session state when checkboxes change
document.addEventListener('DOMContentLoaded', function() {
    // Add change listeners to checkboxes
    const runAnalysisCheckbox = document.querySelector('input[data-testid="stCheckbox"][aria-label="Run analysis"]');
    const applyMaskCheckbox = document.querySelector('input[data-testid="stCheckbox"][aria-label="Apply mask"]');
    
    if (runAnalysisCheckbox) {
        runAnalysisCheckbox.addEventListener('change', function() {
            console.log('Run analysis:', this.checked);
        });
    }
    
    if (applyMaskCheckbox) {
        applyMaskCheckbox.addEventListener('change', function() {
            console.log('Apply mask:', this.checked);
        });
    }
    
    // Update status tags based on checkbox state
    function updateStatusTags() {
        const maskStatus = document.querySelector('.status-tag:nth-child(3)');
        if (applyMaskCheckbox && !applyMaskCheckbox.checked) {
            if (maskStatus) maskStatus.textContent = 'mask: off';
        }
    }
    
    // Initial update
    updateStatusTags();
    
    // Update on checkbox change
    if (applyMaskCheckbox) {
        applyMaskCheckbox.addEventListener('change', updateStatusTags);
    }
});
</script>
""", unsafe_allow_html=True)

# Initialize Earth Engine functionality in background
if st.session_state.ee_initialized:
    try:
        from earth_engine_utils import get_admin_boundaries, get_boundary_names
        st.session_state.ee_ready = True
    except:
        st.session_state.ee_ready = False
else:
    st.session_state.ee_ready = False

# Store session state values
st.session_state.area_name = area_name
st.session_state.selected_veg_index = selected_index
st.session_state.cloud_max = cloud_cover
st.session_state.run_analysis = run_analysis
st.session_state.apply_mask = apply_mask

# Handle analysis if triggered
if 'analysis_triggered' in st.session_state and st.session_state.analysis_triggered:
    # Generate mock analysis results
    import random
    dates = []
    values = []
    
    # Generate 12 months of mock data
    for i in range(12):
        date = datetime(2024, 1, 1) + timedelta(days=30*i)
        dates.append(date.strftime('%Y-%m-%d'))
        # Simulate seasonal vegetation pattern
        value = 0.3 + 0.3 * abs(math.sin(i * math.pi / 6)) + random.uniform(-0.05, 0.05)
        values.append(round(value, 3))
    
    st.session_state.analysis_results = {
        'index': selected_index,
        'dates': dates,
        'values': values,
        'area': area_name,
        'cloud_cover': cloud_cover,
        'mask_applied': apply_mask
    }
    
    # Reset trigger
    st.session_state.analysis_triggered = False

# Show analysis results if available
if 'analysis_results' in st.session_state and st.session_state.analysis_results:
    # Display results in a subtle way
    results = st.session_state.analysis_results
    st.markdown(f"""
    <div style="position: fixed; bottom: 20px; right: 20px; background: var(--bg-secondary); 
                border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; 
                max-width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 1000;">
        <h4 style="margin: 0 0 8px 0; color: var(--text-primary);">Analysis Complete</h4>
        <p style="margin: 4px 0; font-size: 13px; color: var(--text-secondary);">
            <strong>Area:</strong> {results['area']}<br>
            <strong>Index:</strong> {results['index']}<br>
            <strong>Period:</strong> 12 months<br>
            <strong>Avg Value:</strong> {sum(results['values']) / len(results['values']):.3f}
        </p>
        <button onclick="this.parentElement.style.display='none'" 
                style="margin-top: 8px; padding: 4px 12px; background: var(--button-bg); 
                       color: white; border: none; border-radius: 4px; font-size: 12px; 
                       cursor: pointer;">
            Dismiss
        </button>
    </div>
    
    <script>
    // Auto-dismiss after 10 seconds
    setTimeout(function() {{
        const notice = document.querySelector('div[style*="position: fixed; bottom: 20px;"]');
        if (notice) notice.style.display = 'none';
    }}, 10000);
    </script>
    """, unsafe_allow_html=True)

import math
