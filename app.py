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

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'ee_initialized' not in st.session_state:
    st.session_state.ee_initialized = False
if 'selected_geometry' not in st.session_state:
    st.session_state.selected_geometry = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'selected_coordinates' not in st.session_state:
    st.session_state.selected_coordinates = None
if 'selected_area_name' not in st.session_state:
    st.session_state.selected_area_name = None
if 'map_style' not in st.session_state:
    st.session_state.map_style = "satellite"  # satellite, street, dark, terrain

# Page configuration
st.set_page_config(
    page_title="Khisba GIS - 3D Global Vegetation Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Authentication check
if not st.session_state.authenticated:
    st.markdown("""
    <div class="main-container">
        <div class="content-container" style="max-width: 500px; margin: 100px auto;">
            <div class="card">
                <h1 style="text-align: center; margin-bottom: 10px;">🌍 KHISBA GIS</h1>
                <p style="text-align: center; color: #999999; margin-bottom: 30px;">3D Global Vegetation Analytics</p>
                
                <div class="alert alert-warning" style="text-align: center;">
                    🔐 Authentication Required
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
        <p style="color: #999999; margin: 0; font-size: 14px;">Interactive 3D Global Vegetation Analytics</p>
    </div>
    <div style="display: flex; gap: 10px;">
        <span class="status-badge">Connected</span>
        <span class="status-badge">3D Mapbox Globe</span>
        <span class="status-badge">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Helper Functions for Earth Engine
def get_admin_boundaries(level, country_code=None, admin1_code=None):
    """Get administrative boundaries from Earth Engine"""
    try:
        if level == 0:
            return ee.FeatureCollection("FAO/GAUL/2015/level0")
        elif level == 1:
            admin1 = ee.FeatureCollection("FAO/GAUL/2015/level1")
            if country_code:
                return admin1.filter(ee.Filter.eq('ADM0_CODE', country_code))
            return admin1
        elif level == 2:
            admin2 = ee.FeatureCollection("FAO/GAUL/2015/level2")
            if admin1_code:
                return admin2.filter(ee.Filter.eq('ADM1_CODE', admin1_code))
            elif country_code:
                return admin2.filter(ee.Filter.eq('ADM0_CODE', country_code))
            return admin2
    except Exception as e:
        st.error(f"Error loading boundaries: {str(e)}")
        return None

def get_boundary_names(feature_collection, level):
    """Extract boundary names from Earth Engine FeatureCollection"""
    try:
        if level == 0:
            names = feature_collection.aggregate_array('ADM0_NAME').distinct()
        elif level == 1:
            names = feature_collection.aggregate_array('ADM1_NAME').distinct()
        elif level == 2:
            names = feature_collection.aggregate_array('ADM2_NAME').distinct()
        else:
            return []
        
        names_list = names.getInfo()
        if names_list:
            return sorted(names_list)
        return []
        
    except Exception as e:
        st.error(f"Error extracting names: {str(e)}")
        return []

def get_geometry_coordinates(geometry):
    """Get center coordinates and bounds from geometry"""
    try:
        bounds = geometry.geometry().bounds().getInfo()
        coords = bounds['coordinates'][0]
        lats = [coord[1] for coord in coords]
        lons = [coord[0] for coord in coords]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Get bounds for drawing rectangle
        min_lat = min(lats)
        max_lat = max(lats)
        min_lon = min(lons)
        max_lon = max(lons)
        
        return {
            'center': [center_lon, center_lat],
            'bounds': [[min_lat, min_lon], [max_lat, max_lon]],
            'zoom': 6
        }
    except Exception as e:
        st.error(f"Error getting coordinates: {str(e)}")
        return {'center': [0, 20], 'bounds': None, 'zoom': 2}

# VEGETATION INDICES FUNCTIONS
def mask_clouds(image):
    """Mask clouds in Sentinel-2 imagery"""
    try:
        # Sentinel-2 cloud masking
        qa = image.select('QA60')
        cloud_bitmask = 1 << 10
        cirrus_bitmask = 1 << 11
        mask = qa.bitwiseAnd(cloud_bitmask).eq(0).And(
            qa.bitwiseAnd(cirrus_bitmask).eq(0))
        return image.updateMask(mask)
    except Exception as e:
        st.error(f"Error in cloud masking: {str(e)}")
        return image

def add_vegetation_indices(image):
    """Add ALL vegetation indices to an image"""
    try:
        # Define band names based on collection
        if 'SR_B2' in image.bandNames().getInfo():  # Landsat
            blue = image.select('SR_B2')
            green = image.select('SR_B3')
            red = image.select('SR_B4')
            nir = image.select('SR_B5')
            swir1 = image.select('SR_B6')
            swir2 = image.select('SR_B7')
        else:  # Sentinel-2
            blue = image.select('B2')
            green = image.select('B3')
            red = image.select('B4')
            red_edge1 = image.select('B5')
            red_edge2 = image.select('B6')
            red_edge3 = image.select('B7')
            nir = image.select('B8')
            nir_narrow = image.select('B8A')
            swir1 = image.select('B11')
            swir2 = image.select('B12')
        
        # Store all indices
        indices = []
        
        # 1. NDVI - Normalized Difference Vegetation Index
        ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
        indices.append(ndvi)
        
        # 2. EVI - Enhanced Vegetation Index
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
            {'NIR': nir, 'RED': red, 'BLUE': blue}
        ).rename('EVI')
        indices.append(evi)
        
        # 3. SAVI - Soil Adjusted Vegetation Index
        savi = image.expression(
            '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
            {'NIR': nir, 'RED': red}
        ).rename('SAVI')
        indices.append(savi)
        
        # 4. NDWI - Normalized Difference Water Index
        ndwi = green.subtract(nir).divide(green.add(nir)).rename('NDWI')
        indices.append(ndwi)
        
        # 5. GNDVI - Green NDVI
        gndvi = nir.subtract(green).divide(nir.add(green)).rename('GNDVI')
        indices.append(gndvi)
        
        # 6. MSAVI - Modified Soil Adjusted Vegetation Index
        msavi = image.expression(
            '(2 * NIR + 1 - sqrt(pow((2 * NIR + 1), 2) - 8 * (NIR - RED))) / 2',
            {'NIR': nir, 'RED': red}
        ).rename('MSAVI')
        indices.append(msavi)
        
        # 7. ARVI - Atmospherically Resistant Vegetation Index
        arvi = image.expression(
            '(NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE))',
            {'NIR': nir, 'RED': red, 'BLUE': blue}
        ).rename('ARVI')
        indices.append(arvi)
        
        # 8. EVI2 - 2-band Enhanced Vegetation Index
        evi2 = image.expression(
            '2.5 * (NIR - RED) / (NIR + 2.4 * RED + 1)',
            {'NIR': nir, 'RED': red}
        ).rename('EVI2')
        indices.append(evi2)
        
        # 9. OSAVI - Optimized Soil Adjusted Vegetation Index
        osavi = image.expression(
            '1.16 * (NIR - RED) / (NIR + RED + 0.16)',
            {'NIR': nir, 'RED': red}
        ).rename('OSAVI')
        indices.append(osavi)
        
        # 10. NDMI - Normalized Difference Moisture Index
        ndmi = nir.subtract(swir1).divide(nir.add(swir1)).rename('NDMI')
        indices.append(ndmi)
        
        # 11. MNDWI - Modified NDWI
        mndwi = green.subtract(swir1).divide(green.add(swir1)).rename('MNDWI')
        indices.append(mndwi)
        
        # 12. VARI - Visible Atmospherically Resistant Index
        vari = image.expression(
            '(GREEN - RED) / (GREEN + RED - BLUE)',
            {'GREEN': green, 'RED': red, 'BLUE': blue}
        ).rename('VARI')
        indices.append(vari)
        
        # 13. TVI - Transformed Vegetation Index
        tvi = image.expression(
            'sqrt((NIR - RED) / (NIR + RED) + 0.5)',
            {'NIR': nir, 'RED': red}
        ).rename('TVI')
        indices.append(tvi)
        
        # 14. GCVI - Green Chlorophyll Vegetation Index
        gcvi = image.expression(
            '(NIR / GREEN) - 1',
            {'NIR': nir, 'GREEN': green}
        ).rename('GCVI')
        indices.append(gcvi)
        
        # 15. NBR - Normalized Burn Ratio
        nbr = nir.subtract(swir2).divide(nir.add(swir2)).rename('NBR')
        indices.append(nbr)
        
        # 16. CVI - Chlorophyll Vegetation Index
        cvi = image.expression(
            'NIR * (RED / pow(GREEN, 2))',
            {'NIR': nir, 'RED': red, 'GREEN': green}
        ).rename('CVI')
        indices.append(cvi)
        
        # 17. RI - Redness Index
        ri = image.expression(
            'RED / GREEN',
            {'RED': red, 'GREEN': green}
        ).rename('RI')
        indices.append(ri)
        
        # 18. CI - Coloration Index
        ci = image.expression(
            '(RED - GREEN) / (RED + GREEN)',
            {'RED': red, 'GREEN': green}
        ).rename('CI')
        indices.append(ci)
        
        # 19. BI - Brightness Index
        bi = image.expression(
            'sqrt(pow(GREEN, 2) + pow(RED, 2))',
            {'GREEN': green, 'RED': red}
        ).rename('BI')
        indices.append(bi)
        
        # 20. SI - Soil Index
        si = image.expression(
            '(RED - BLUE) / (RED + BLUE)',
            {'RED': red, 'BLUE': blue}
        ).rename('SI')
        indices.append(si)
        
        return image.addBands(indices)
        
    except Exception as e:
        st.error(f"Error adding vegetation indices: {str(e)}")
        return image

# Map Style Toggle
col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 2, 1])
with col_toggle2:
    st.markdown('<div class="view-toggle">', unsafe_allow_html=True)
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        if st.button("🛰️ Satellite", use_container_width=True, key="satellite_btn"):
            st.session_state.map_style = "satellite"
            st.rerun()
    with col_b:
        if st.button("🗺️ Streets", use_container_width=True, key="streets_btn"):
            st.session_state.map_style = "street"
            st.rerun()
    with col_c:
        if st.button("🏔️ Terrain", use_container_width=True, key="terrain_btn"):
            st.session_state.map_style = "terrain"
            st.rerun()
    with col_d:
        if st.button("🌙 Dark", use_container_width=True, key="dark_btn"):
            st.session_state.map_style = "dark"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Create main layout containers
col1, col2 = st.columns([0.25, 0.75], gap="large")

# LEFT SIDEBAR - All controls
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">🌍</div><h3 style="margin: 0;">Area Selection</h3></div>', unsafe_allow_html=True)
    
    if st.session_state.ee_initialized:
        try:
            # Get countries
            countries_fc = get_admin_boundaries(0)
            if countries_fc:
                country_names = get_boundary_names(countries_fc, 0)
                selected_country = st.selectbox(
                    "Country",
                    options=["Select a country"] + country_names,
                    index=0,
                    help="Choose a country for analysis",
                    key="country_select"
                )
                
                if selected_country and selected_country != "Select a country":
                    # Get country code
                    country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first()
                    
                    # Get admin1 regions for selected country
                    admin1_fc = get_admin_boundaries(1, country_feature.get('ADM0_CODE').getInfo())
                    if admin1_fc:
                        admin1_names = get_boundary_names(admin1_fc, 1)
                        selected_admin1 = st.selectbox(
                            "State/Province",
                            options=["Select state/province"] + admin1_names,
                            index=0,
                            help="Choose a state or province",
                            key="admin1_select"
                        )
                        
                        if selected_admin1 and selected_admin1 != "Select state/province":
                            # Get admin1 code
                            admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
                            
                            # Get admin2 regions for selected admin1
                            admin2_fc = get_admin_boundaries(2, None, admin1_feature.get('ADM1_CODE').getInfo())
                            if admin2_fc:
                                admin2_names = get_boundary_names(admin2_fc, 2)
                                selected_admin2 = st.selectbox(
                                    "Municipality",
                                    options=["Select municipality"] + admin2_names,
                                    index=0,
                                    help="Choose a municipality",
                                    key="admin2_select"
                                )
                            else:
                                selected_admin2 = None
                        else:
                            selected_admin2 = None
                    else:
                        selected_admin1 = None
                        selected_admin2 = None
                else:
                    selected_admin1 = None
                    selected_admin2 = None
            else:
                st.error("Failed to load countries. Please check Earth Engine connection.")
                selected_country = None
                selected_admin1 = None
                selected_admin2 = None
                
        except Exception as e:
            st.error(f"Error loading boundaries: {str(e)}")
            selected_country = None
            selected_admin1 = None
            selected_admin2 = None
    else:
        st.warning("Earth Engine not initialized")
        selected_country = None
        selected_admin1 = None
        selected_admin2 = None
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update selected geometry when area is selected
    if selected_country and selected_country != "Select a country":
        try:
            # Determine geometry
            if selected_admin2 and selected_admin2 != "Select municipality":
                geometry = admin2_fc.filter(ee.Filter.eq('ADM2_NAME', selected_admin2))
                area_name = f"{selected_admin2}, {selected_admin1}, {selected_country}"
                area_level = "Municipality"
            elif selected_admin1 and selected_admin1 != "Select state/province":
                geometry = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1))
                area_name = f"{selected_admin1}, {selected_country}"
                area_level = "State/Province"
            else:
                geometry = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country))
                area_name = selected_country
                area_level = "Country"
            
            # Get coordinates for the map
            coords_info = get_geometry_coordinates(geometry)
            
            # Store in session state
            st.session_state.selected_geometry = geometry
            st.session_state.selected_coordinates = coords_info
            st.session_state.selected_area_name = area_name
            st.session_state.selected_area_level = area_level
            
        except Exception as e:
            st.error(f"Error processing geometry: {str(e)}")
    
    # Analysis Parameters Card
    if selected_country and selected_country != "Select a country":
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
        
        # ALL vegetation indices available
        available_indices = [
            'NDVI', 'EVI', 'SAVI', 'NDWI', 'GNDVI', 'MSAVI', 'ARVI', 'EVI2', 'OSAVI', 
            'NDMI', 'MNDWI', 'VARI', 'TVI', 'GCVI', 'NBR', 'CVI', 'RI', 'CI', 'BI', 'SI'
        ]
        
        selected_indices = st.multiselect(
            "Select Indices",
            options=available_indices,
            default=['NDVI', 'EVI', 'SAVI', 'NDWI', 'GNDVI'],
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
                            .filterBounds(st.session_state.selected_geometry.geometry())
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
                                        scale=100,
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

# MAIN CONTENT AREA - 3D Mapbox Globe with Selected Area Highlight
with col2:
    # 3D Mapbox Globe
    st.markdown('<div class="card" style="padding: 0;">', unsafe_allow_html=True)
    st.markdown('<div style="padding: 20px 20px 10px 20px;"><h3 style="margin: 0;">Interactive 3D Global Map</h3></div>', unsafe_allow_html=True)
    
    # Prepare coordinates for the map
    map_center = [0, 20]
    map_zoom = 2
    bounds_data = None
    
    if st.session_state.selected_coordinates:
        map_center = st.session_state.selected_coordinates['center']
        map_zoom = st.session_state.selected_coordinates['zoom']
        bounds_data = st.session_state.selected_coordinates['bounds']
    
    # Map style mapping
    map_styles = {
        "satellite": "mapbox://styles/mapbox/satellite-streets-v12",
        "street": "mapbox://styles/mapbox/streets-v12",
        "terrain": "mapbox://styles/mapbox/outdoors-v12",
        "dark": "mapbox://styles/mapbox/dark-v11"
    }
    
    current_style = map_styles[st.session_state.map_style]
    
    # Generate HTML for Mapbox interactive globe
    mapbox_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
      <title>KHISBA GIS - 3D Global Map</title>
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
        .map-overlay {{
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
        .overlay-title {{
          color: #00ff88;
          font-weight: 600;
          margin-bottom: 10px;
          font-size: 14px;
        }}
        .overlay-text {{
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
        .selected-area {{
          position: absolute;
          top: 20px;
          left: 20px;
          background: rgba(10, 10, 10, 0.9);
          color: white;
          padding: 15px;
          border-radius: 8px;
          border: 1px solid #222222;
          max-width: 300px;
          z-index: 1000;
          font-family: 'Inter', sans-serif;
        }}
        .area-title {{
          color: #00ff88;
          font-weight: 600;
          margin-bottom: 10px;
          font-size: 14px;
        }}
        .area-details {{
          color: #cccccc;
          font-size: 12px;
          line-height: 1.4;
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
        .city-marker {{
          background-color: #ffaa00;
          width: 15px;
          height: 15px;
          border-radius: 50%;
          border: 2px solid #ffffff;
          box-shadow: 0 0 10px rgba(255, 170, 0, 0.5);
          cursor: pointer;
          transition: all 0.3s;
        }}
        .city-marker:hover {{
          transform: scale(1.3);
          box-shadow: 0 0 15px rgba(255, 170, 0, 0.8);
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      
      <div class="map-overlay">
        <div class="overlay-title">🌍 KHISBA GIS</div>
        <div class="overlay-text">
          • Drag to rotate the globe<br>
          • Scroll to zoom in/out<br>
          • Right-click to pan<br>
          • Selected area highlighted in green
        </div>
      </div>
      
      <div class="coordinates-display">
        <div>Lat: <span id="lat-display">0.00°</span></div>
        <div>Lon: <span id="lon-display">0.00°</span></div>
      </div>
      
      {f'''
      <div class="selected-area">
        <div class="area-title">📍 Selected Area</div>
        <div class="area-details">
          <strong>{st.session_state.selected_area_name if hasattr(st.session_state, 'selected_area_name') else 'None'}</strong><br>
          Level: {st.session_state.selected_area_level if hasattr(st.session_state, 'selected_area_level') else 'None'}<br>
          Coordinates: {map_center[1]:.4f}°, {map_center[0]:.4f}°<br>
          Status: <span style="color: #00ff88;">Ready for Analysis</span>
        </div>
      </div>
      ''' if st.session_state.selected_area_name else ''}
      
      <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiYnJ5Y2VseW5uMjUiLCJhIjoiY2x1a2lmcHh5MGwycTJrbzZ4YXVrb2E0aiJ9.LXbneMJJ6OosHv9ibtI5XA';

        // Create a new map instance
        const map = new mapboxgl.Map({{
          container: 'map',
          style: '{current_style}',
          center: {map_center},
          zoom: {map_zoom},
          pitch: 45,
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

        // Wait for map to load
        map.on('load', () => {{
          // Add event listener for mouse move to show coordinates
          map.on('mousemove', (e) => {{
            document.getElementById('lat-display').textContent = e.lngLat.lat.toFixed(2) + '°';
            document.getElementById('lon-display').textContent = e.lngLat.lng.toFixed(2) + '°';
          }});

          // Add selected area polygon if bounds are available
          {f'''
          if ({bounds_data}) {{
            const bounds = {bounds_data};
            
            // Create a polygon for the selected area
            map.addSource('selected-area', {{
              'type': 'geojson',
              'data': {{
                'type': 'Feature',
                'geometry': {{
                  'type': 'Polygon',
                  'coordinates': [[
                    [bounds[0][1], bounds[0][0]],
                    [bounds[1][1], bounds[0][0]],
                    [bounds[1][1], bounds[1][0]],
                    [bounds[0][1], bounds[1][0]],
                    [bounds[0][1], bounds[0][0]]
                  ]]
                }}
              }}
            }});

            // Add the polygon layer
            map.addLayer({{
              'id': 'selected-area-fill',
              'type': 'fill',
              'source': 'selected-area',
              'layout': {{}},
              'paint': {{
                'fill-color': '#00ff88',
                'fill-opacity': 0.2
              }}
            }});

            // Add border for the polygon
            map.addLayer({{
              'id': 'selected-area-border',
              'type': 'line',
              'source': 'selected-area',
              'layout': {{}},
              'paint': {{
                'line-color': '#00ff88',
                'line-width': 3,
                'line-opacity': 0.8
              }}
            }});

            // Fly to the selected area with animation
            map.flyTo({{
              center: {map_center},
              zoom: {map_zoom},
              duration: 2000,
              essential: true
            }});
          }}
          ''' if bounds_data else ''}

          // Add major cities with interactive markers
          const cities = [
            {{ name: 'New York', coordinates: [-74.006, 40.7128], country: 'USA', info: 'Financial capital of the world' }},
            {{ name: 'London', coordinates: [-0.1276, 51.5074], country: 'UK', info: 'Historical and cultural capital' }},
            {{ name: 'Tokyo', coordinates: [139.6917, 35.6895], country: 'Japan', info: 'Mega metropolis with advanced technology' }},
            {{ name: 'Sydney', coordinates: [151.2093, -33.8688], country: 'Australia', info: 'Major harbor city with iconic opera house' }},
            {{ name: 'Cairo', coordinates: [31.2357, 30.0444], country: 'Egypt', info: 'Ancient city on the Nile Delta' }},
            {{ name: 'Rio de Janeiro', coordinates: [-43.1729, -22.9068], country: 'Brazil', info: 'Famous for Carnival and beaches' }},
            {{ name: 'Moscow', coordinates: [37.6173, 55.7558], country: 'Russia', info: 'Historic city with Red Square' }},
            {{ name: 'Dubai', coordinates: [55.2708, 25.2048], country: 'UAE', info: 'Modern metropolis in the desert' }},
            {{ name: 'Singapore', coordinates: [103.8198, 1.3521], country: 'Singapore', info: 'Garden city and financial hub' }},
            {{ name: 'Cape Town', coordinates: [18.4241, -33.9249], country: 'South Africa', info: 'Coastal city with Table Mountain' }}
          ];

          // Add city markers with fly-to animation
          cities.forEach(city => {{
            // Create a custom marker element
            const el = document.createElement('div');
            el.className = 'city-marker';
            el.title = city.name;

            // Create a popup
            const popup = new mapboxgl.Popup({{
              offset: 25,
              closeButton: true,
              closeOnClick: false
            }}).setHTML(
              `<h3>{city.name}</h3>
               <p><strong>Country:</strong> {city.country}</p>
               <p>{city.info}</p>
               <p><strong>Coordinates:</strong><br>
               Lat: {city.coordinates[1].toFixed(4)}°<br>
               Lon: {city.coordinates[0].toFixed(4)}°</p>`
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

          // Handle region fly from Streamlit
          const regions = {{
            usa: {{ center: [-95.7129, 37.0902], zoom: 3 }},
            europe: {{ center: [15.2551, 54.5260], zoom: 3 }},
            asia: {{ center: [104.1954, 35.8617], zoom: 2 }},
            americas: {{ center: [-58.3816, -14.2350], zoom: 2 }},
            reset: {{ center: [0, 20], zoom: 2 }}
          }};

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
        }});
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
        if results:
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
                            # Parse dates
                            dates = []
                            for date_str in data['dates']:
                                try:
                                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                    dates.append(date_obj)
                                except:
                                    continue
                            
                            values = [v for v in data['values'] if v is not None]
                            
                            if dates and values and len(dates) == len(values):
                                df = pd.DataFrame({'Date': dates, 'Value': values})
                                df = df.sort_values('Date')
                                
                                # Calculate analytical metrics
                                df['MA_5'] = df['Value'].rolling(window=min(5, len(df))).mean()
                                df['MA_10'] = df['Value'].rolling(window=min(10, len(df))).mean()
                                
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
                                        tilecolor='#444444',
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

# Footer
st.markdown("""
<div class="section-divider"></div>
<div style="text-align: center; color: #666666; font-size: 12px; padding: 20px 0;">
    <p style="margin: 5px 0;">KHISBA GIS • Interactive 3D Global Vegetation Analytics Platform</p>
    <p style="margin: 5px 0;">Created by Taibi Farouk Djilali • Clean Green & Black Design</p>
</div>
""", unsafe_allow_html=True)
