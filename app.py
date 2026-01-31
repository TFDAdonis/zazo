import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ee
import traceback
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

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
        padding-top: 2rem;
        padding-bottom: 2rem;
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
    
    /* PyDeck/WebGL Map Container */
    .deckgl-wrapper {
        border: 1px solid var(--border-gray);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    
    /* 3D Earth Controls */
    .earth-controls {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(10, 10, 10, 0.9);
        border: 1px solid var(--border-gray);
        border-radius: 8px;
        padding: 15px;
        min-width: 200px;
        backdrop-filter: blur(10px);
    }
    
    .control-group {
        margin-bottom: 15px;
    }
    
    .control-label {
        color: var(--text-gray);
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 5px;
        display: block;
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

# Page configuration
st.set_page_config(
    page_title="Khisba GIS - 3D Earth Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'ee_initialized' not in st.session_state:
    st.session_state.ee_initialized = False
if 'selected_geometry' not in st.session_state:
    st.session_state.selected_geometry = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Authentication check
if not st.session_state.authenticated:
    st.markdown("""
    <div style="max-width: 500px; margin: 100px auto;">
        <div class="card">
            <h1 style="text-align: center; margin-bottom: 10px;">KHISBA GIS</h1>
            <p style="text-align: center; color: #999999; margin-bottom: 30px;">Professional 3D Earth Analytics</p>
            
            <div style="padding: 15px; background: rgba(255, 170, 0, 0.1); border: 1px solid rgba(255, 170, 0, 0.3); border-radius: 8px; margin-bottom: 20px; text-align: center;">
                🔐 Authentication Required
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
    <div style="max-width: 500px; margin: 30px auto;">
        <div class="card">
            <p style="text-align: center; color: #00ff88; font-weight: 600; margin-bottom: 10px;">3D Earth Demo Access</p>
            <p style="text-align: center; color: #999999;">Use <strong>admin</strong> / <strong>admin</strong> for demo</p>
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                <span class="status-badge">WebGL 3D</span>
                <span class="status-badge">Earth Engine</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Main Dashboard Layout
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
    <div>
        <h1>🌍 KHISBA GIS</h1>
        <p style="color: #999999; margin: 0; font-size: 14px;">Professional 3D Earth Observation & Analytics</p>
    </div>
    <div style="display: flex; gap: 10px;">
        <span class="status-badge">WebGL 3D</span>
        <span class="status-badge">Connected</span>
        <span class="status-badge">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

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
        st.markdown('<div class="card-title"><div class="icon">⚙️</div><h3 style="margin: 0;">3D Earth Settings</h3></div>', unsafe_allow_html=True)
        
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
            options=["Sentinel-2", "Landsat-8", "MODIS"],
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
        
        # 3D View Settings
        view_3d = st.checkbox("Enable 3D Terrain", value=True, key="view_3d")
        if view_3d:
            terrain_exaggeration = st.slider(
                "Terrain Exaggeration",
                min_value=1.0,
                max_value=10.0,
                value=3.0,
                step=0.5,
                help="Height exaggeration for 3D terrain"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Vegetation Indices Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">🌿</div><h3 style="margin: 0;">Vegetation Indices</h3></div>', unsafe_allow_html=True)
        
        available_indices = [
            'NDVI', 'EVI', 'SAVI', 'NDWI', 'GNDVI', 'MSAVI', 'NDMI'
        ]
        
        selected_indices = st.multiselect(
            "Select Indices",
            options=available_indices,
            default=['NDVI', 'EVI', 'SAVI'],
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
        
        # 3D Layer Controls Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">🛰️</div><h3 style="margin: 0;">3D Earth Layers</h3></div>', unsafe_allow_html=True)
        
        # Map style
        map_style = st.selectbox(
            "Earth Style",
            options=["Satellite", "Dark", "Light", "Terrain", "Night"],
            help="Choose the Earth visualization style",
            key="map_style"
        )
        
        # Layer controls
        col_e, col_f = st.columns(2)
        with col_e:
            show_vegetation_layer = st.checkbox("Vegetation", value=True, key="show_veg")
            show_temperature = st.checkbox("Temperature", value=False, key="show_temp")
            show_population = st.checkbox("Population", value=False, key="show_pop")
        with col_f:
            show_night_lights = st.checkbox("Night Lights", value=False, key="show_night")
            show_elevation = st.checkbox("Elevation", value=True, key="show_elev")
            show_borders = st.checkbox("Borders", value=True, key="show_borders")
        
        # Map rotation
        auto_rotate = st.checkbox("Auto-Rotate Earth", value=False, key="auto_rotate")
        if auto_rotate:
            rotation_speed = st.slider(
                "Rotation Speed",
                min_value=1,
                max_value=10,
                value=3,
                help="Earth rotation speed"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Run Analysis Button
        if st.button("🚀 Run 3D Earth Analysis", type="primary", use_container_width=True, key="run_analysis"):
            if not selected_indices:
                st.error("Please select at least one vegetation index")
            else:
                with st.spinner("Running 3D Earth analysis..."):
                    try:
                        # Define collection based on choice
                        if collection_choice == "Sentinel-2":
                            collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                        elif collection_choice == "Landsat-8":
                            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                        else:
                            collection = ee.ImageCollection('MODIS/006/MOD13Q1')
                        
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
                        st.success("✅ 3D Earth analysis completed!")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")

# MAIN CONTENT AREA - 3D Earth View and Results
with col2:
    # 3D Earth View Display
    if selected_country:
        st.markdown('<div class="card" style="padding: 0;">', unsafe_allow_html=True)
        st.markdown('<div style="padding: 20px 20px 10px 20px;"><h3 style="margin: 0;">🌍 WebGL 3D Earth View</h3></div>', unsafe_allow_html=True)
        
        try:
            # Determine geometry and center
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
            
            # Get center coordinates
            bounds = geometry.geometry().bounds().getInfo()
            coords = bounds['coordinates'][0]
            lats = [coord[1] for coord in coords]
            lons = [coord[0] for coord in coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
            
            st.session_state.selected_geometry = geometry
            
            # Create sample data for 3D visualization
            # In production, you would fetch actual terrain/elevation data
            n_points = 100
            lats_range = np.linspace(min(lats), max(lats), n_points)
            lons_range = np.linspace(min(lons), max(lons), n_points)
            
            # Create grid data
            data = []
            for lat in lats_range:
                for lon in lons_range:
                    # Simulate elevation data (in production, use actual DEM)
                    elevation = np.random.normal(100, 50)
                    # Add vegetation index simulation
                    ndvi = 0.3 + 0.5 * np.sin(lat * 0.1) * np.cos(lon * 0.1)
                    
                    data.append({
                        'lat': lat,
                        'lon': lon,
                        'elevation': max(0, elevation),
                        'ndvi': ndvi,
                        'temperature': 20 + 10 * np.sin(lat * 0.05)
                    })
            
            df = pd.DataFrame(data)
            
            # Determine map style
            map_styles = {
                "Satellite": "mapbox://styles/mapbox/satellite-v9",
                "Dark": "mapbox://styles/mapbox/dark-v10",
                "Light": "mapbox://styles/mapbox/light-v10",
                "Terrain": "mapbox://styles/mapbox/outdoors-v11",
                "Night": "mapbox://styles/mapbox/navigation-night-v1"
            }
            
            selected_style = map_styles.get(map_style, map_styles["Dark"])
            
            # Create 3D terrain layer
            terrain_layer = pdk.Layer(
                "HexagonLayer",
                df,
                get_position=['lon', 'lat'],
                get_elevation='elevation',
                elevation_scale=terrain_exaggeration if 'terrain_exaggeration' in locals() else 3,
                extruded=True,
                radius=200,
                opacity=0.6,
                coverage=1,
                elevation_range=[0, 300],
                pickable=True,
                auto_highlight=True,
                get_fill_color='[255 * ndvi, 255 * (1 - ndvi), 0, 200]' if show_vegetation_layer else '[200, 200, 200, 200]'
            )
            
            # Create grid layer for area boundaries
            grid_layer = pdk.Layer(
                "GridLayer",
                df,
                get_position=['lon', 'lat'],
                cell_size=5000,
                elevation_scale=50,
                pickable=True,
                auto_highlight=True,
                get_fill_color='[0, 255, 136, 100]' if show_borders else '[0, 0, 0, 0]'
            )
            
            # Create heatmap layer for temperature
            if show_temperature:
                temp_layer = pdk.Layer(
                    "HeatmapLayer",
                    df,
                    get_position=['lon', 'lat'],
                    get_weight='temperature',
                    radius_pixels=30,
                    intensity=1,
                    threshold=0.1,
                    color_range=[
                        [0, 0, 255, 100],    # Blue - cold
                        [0, 255, 255, 150],  # Cyan
                        [0, 255, 0, 200],    # Green
                        [255, 255, 0, 200],  # Yellow
                        [255, 128, 0, 200],  # Orange
                        [255, 0, 0, 200]     # Red - hot
                    ]
                )
            
            # Configure initial view state
            initial_view_state = pdk.ViewState(
                latitude=center_lat,
                longitude=center_lon,
                zoom=6,
                pitch=45 if view_3d else 0,
                bearing=0
            )
            
            # Create the deck
            layers = [terrain_layer, grid_layer]
            if show_temperature and 'temp_layer' in locals():
                layers.append(temp_layer)
            
            deck = pdk.Deck(
                layers=layers,
                initial_view_state=initial_view_state,
                map_style=selected_style,
                tooltip={
                    "html": """
                    <b>Lat:</b> {lat:.4f}<br/>
                    <b>Lon:</b> {lon:.4f}<br/>
                    <b>Elevation:</b> {elevation:.0f}m<br/>
                    <b>NDVI:</b> {ndvi:.2f}
                    """,
                    "style": {
                        "backgroundColor": "#0a0a0a",
                        "color": "#00ff88",
                        "padding": "10px",
                        "borderRadius": "5px",
                        "border": "1px solid #222"
                    }
                }
            )
            
            # Display the 3D Earth
            st.markdown('<div class="deckgl-wrapper">', unsafe_allow_html=True)
            st.pydeck_chart(deck, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add 3D Earth Controls Overlay
            controls_html = f"""
            <div class="earth-controls">
                <div class="control-group">
                    <div class="control-label">3D EARTH CONTROLS</div>
                    <div style="color: #00ff88; font-size: 11px; margin-top: 5px;">
                        • Drag: Rotate Earth<br/>
                        • Scroll: Zoom In/Out<br/>
                        • Shift + Drag: Pan<br/>
                        • Ctrl + Drag: Tilt
                    </div>
                </div>
                
                <div class="control-group">
                    <div class="control-label">ACTIVE LAYERS</div>
                    <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-top: 5px;">
            """
            
            # Add layer indicators
            if show_vegetation_layer:
                controls_html += '<span class="status-badge" style="font-size: 10px; padding: 2px 8px;">🌿 Veg</span>'
            if show_elevation:
                controls_html += '<span class="status-badge" style="font-size: 10px; padding: 2px 8px;">⛰️ Elev</span>'
            if show_borders:
                controls_html += '<span class="status-badge" style="font-size: 10px; padding: 2px 8px;">🗺️ Borders</span>'
            if show_temperature:
                controls_html += '<span class="status-badge" style="font-size: 10px; padding: 2px 8px;">🌡️ Temp</span>'
            if show_population:
                controls_html += '<span class="status-badge" style="font-size: 10px; padding: 2px 8px;">👥 Pop</span>'
            if show_night_lights:
                controls_html += '<span class="status-badge" style="font-size: 10px; padding: 2px 8px;">🌃 Night</span>'
            
            controls_html += f"""
                    </div>
                </div>
                
                <div class="control-group">
                    <div class="control-label">EARTH INFO</div>
                    <div style="color: #cccccc; font-size: 11px; margin-top: 5px;">
                        View: <span style="color: #00ff88;">{map_style}</span><br/>
                        3D: <span style="color: #00ff88;">{'ON' if view_3d else 'OFF'}</span><br/>
                        Auto-Rotate: <span style="color: #00ff88;">{'ON' if auto_rotate else 'OFF'}</span>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(controls_html, unsafe_allow_html=True)
            
            # Area info panel
            st.markdown(f"""
            <div style="background: #0a0a0a; border: 1px solid #222; border-radius: 8px; padding: 15px; margin-top: 15px;">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;">
                    <div>
                        <div style="color: #999; font-size: 12px; font-weight: 500; margin-bottom: 2px;">🌍 Study Area</div>
                        <div style="color: #fff; font-size: 14px; font-weight: 500;">{area_name}</div>
                    </div>
                    <div>
                        <div style="color: #999; font-size: 12px; font-weight: 500; margin-bottom: 2px;">📏 Level</div>
                        <div style="color: #00ff88; font-size: 14px; font-weight: 500;">{area_level}</div>
                    </div>
                    <div>
                        <div style="color: #999; font-size: 12px; font-weight: 500; margin-bottom: 2px;">📍 Center</div>
                        <div style="color: #fff; font-size: 14px; font-weight: 500;">{center_lat:.4f}°, {center_lon:.4f}°</div>
                    </div>
                    <div>
                        <div style="color: #999; font-size: 12px; font-weight: 500; margin-bottom: 2px;">🛰️ Style</div>
                        <div style="color: #00ff88; font-size: 14px; font-weight: 500;">{map_style}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ 3D Earth View Error: {str(e)}")
            st.info("Loading alternative 2D view...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis Results Section
    if st.session_state.analysis_results:
        st.markdown('<div style="height: 1px; background: #222; margin: 25px 0;"></div>', unsafe_allow_html=True)
        
        # Results Header
        st.markdown('<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;"><h3>🌍 3D Earth Analysis Results</h3><span class="status-badge">Complete</span></div>', unsafe_allow_html=True)
        
        results = st.session_state.analysis_results
        
        # Summary Statistics
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📊</div><h3 style="margin: 0;">Earth Analytics Summary</h3></div>', unsafe_allow_html=True)
        
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
                        'Trend': '📈' if values[-1] > values[0] else '📉'
                    })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3D Visualization of Results
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📈</div><h3 style="margin: 0;">3D Vegetation Analytics</h3></div>', unsafe_allow_html=True)
        
        if selected_indices and len(selected_indices) > 0:
            # Create interactive 3D plot
            index = selected_indices[0]
            data = results[index]
            
            if data['dates'] and data['values']:
                dates = [datetime.fromisoformat(d.replace('Z', '+00:00')) for d in data['dates']]
                values = [v for v in data['values'] if v is not None]
                
                if dates and values and len(dates) == len(values):
                    df = pd.DataFrame({'Date': dates, 'Value': values})
                    df = df.sort_values('Date')
                    
                    # Create 3D surface plot
                    fig = go.Figure(data=[go.Surface(
                        z=np.array([df['Value'].values]),
                        colorscale='greens',
                        showscale=True,
                        hovertemplate='Value: %{z:.4f}<extra></extra>'
                    )])
                    
                    fig.update_layout(
                        title=f'{index} - 3D Surface Analysis',
                        scene=dict(
                            xaxis_title='Time',
                            yaxis_title='Observation',
                            zaxis_title=index,
                            bgcolor='#0a0a0a'
                        ),
                        plot_bgcolor='#0a0a0a',
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff'),
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">💾</div><h3 style="margin: 0;">3D Earth Data Export</h3></div>', unsafe_allow_html=True)
        
        if st.button("📥 Download 3D Analysis Data", type="primary", use_container_width=True, key="export_3d"):
            export_data = []
            for index, data in results.items():
                for date, value in zip(data['dates'], data['values']):
                    if value is not None:
                        export_data.append({
                            'Date': date,
                            'Index': index,
                            'Value': value,
                            'Latitude': center_lat,
                            'Longitude': center_lon,
                            'Area': area_name
                        })
            
            if export_data:
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Download CSV File",
                    data=csv,
                    file_name=f"3d_earth_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for export")

# Status indicators at bottom
if not st.session_state.ee_initialized:
    st.markdown('<div style="padding: 12px 16px; border-radius: 8px; margin: 10px 0; border: 1px solid rgba(255, 170, 0, 0.3); background: #0a0a0a; font-size: 14px; color: #ffaa00;">🌍 Earth Engine initialization required.</div>', unsafe_allow_html=True)
elif st.session_state.selected_geometry is None:
    st.markdown('<div style="padding: 12px 16px; border-radius: 8px; margin: 10px 0; border: 1px solid rgba(255, 170, 0, 0.3); background: #0a0a0a; font-size: 14px; color: #ffaa00;">🌍 Please select a study area to begin 3D Earth analysis.</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="height: 1px; background: #222; margin: 25px 0;"></div>
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px 0;">
    <p style="margin: 5px 0;">🌍 KHISBA GIS • Professional 3D Earth Observation Platform</p>
    <p style="margin: 5px 0;">Created by Taibi Farouk Djilali • WebGL 3D Earth Visualization</p>
    <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px;">
        <span class="status-badge">PyDeck WebGL</span>
        <span class="status-badge">Google Earth Engine</span>
        <span class="status-badge">3D Terrain</span>
        <span class="status-badge">Real-time Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)
