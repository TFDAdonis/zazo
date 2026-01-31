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
import numpy as np

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
    page_icon="📊",
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
if 'map_mode' not in st.session_state:
    st.session_state.map_mode = "globe"  # Default to globe view

# Authentication check
if not st.session_state.authenticated:
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(90deg, #1f4037, #99f2c8); padding: 30px; border-radius: 15px; margin-bottom: 30px;">
    <h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 KHISBA GIS</h1>
    <h3 style="color: #e8f5e8; margin: 10px 0; font-weight: 300;">Professional Vegetation Indices Analytics</h3>
    <p style="color: #ffffff; font-size: 1.1rem; margin: 15px 0 0 0;">Created by <strong>Taibi Farouk Djilali</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Authentication Required")
    st.info("Please enter the admin password to access Khisba GIS")
    
    password = st.text_input("Password", type="password", placeholder="Enter admin password")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔓 LOGIN", type="primary"):
            if password == "admin":
                st.session_state.authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password. Demo password: admin")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; background: #1a1a1a; border-radius: 10px;">
        <h4 style="color: #00ff88; margin: 0;">Demo Access</h4>
        <p style="color: #cccccc; margin: 10px 0 0 0;">Username: <strong>admin</strong><br>Password: <strong>admin</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

st.markdown("""
<div style="text-align: center; background: linear-gradient(90deg, #1f4037, #99f2c8); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
<h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 KHISBA GIS</h1>
<h3 style="color: #e8f5e8; margin: 10px 0 0 0; font-weight: 300;">Professional Vegetation Indices Analytics</h3>
<p style="color: #ffffff; font-size: 1.1rem; margin: 15px 0 0 0;">Created by <strong>Taibi Farouk Djilali</strong></p>
</div>
""", unsafe_allow_html=True)

# Professional Trading Dashboard Sidebar
st.sidebar.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #00ff88, #004422); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="color: white; margin: 0; font-size: 1.5rem;">📊 KHISBA</h2>
    <p style="color: #e8f5e8; margin: 5px 0 0 0; font-size: 0.9rem;">Professional GIS Trading</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🔐 **AUTHENTICATION**")

# Check if Earth Engine is already auto-initialized
if st.session_state.ee_initialized:
    st.sidebar.success("✅ Earth Engine Connected (Auto-Authenticated)")
else:
    st.sidebar.subheader("Upload GEE Credentials")
    st.sidebar.markdown("**Required:** Google Earth Engine service account JSON file")
    st.sidebar.markdown("""
    **Steps to get your credentials:**
    1. Go to [Google Cloud Console](https://console.cloud.google.com)
    2. Select your project and go to IAM & Admin → Service Accounts  
    3. Create or select a service account
    4. Click "Add Key" → "Create new key" → JSON
    5. Download and upload the JSON file here
    
    **Note:** Your project must be registered with Earth Engine at [signup.earthengine.google.com](https://signup.earthengine.google.com)
    """)
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose your service account JSON file",
        type=['json'],
        help="Upload your Google Earth Engine service account JSON credentials"
    )
    
    if uploaded_file is not None:
        try:
            # Read and parse the JSON file
            credentials_data = json.load(uploaded_file)
            
            # Save credentials to a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                json.dump(credentials_data, tmp_file)
                credentials_path = tmp_file.name
            
            # Import and use the original initialize_earth_engine function
            from earth_engine_utils import initialize_earth_engine
            success = initialize_earth_engine(credentials_path)
            
            if success:
                st.session_state.ee_initialized = True
                st.session_state.credentials_uploaded = True
                st.sidebar.success("✅ Earth Engine initialized successfully!")
                
                # Clean up temporary file
                os.unlink(credentials_path)
                st.rerun()
            else:
                st.sidebar.error("❌ Failed to initialize Earth Engine")
                st.sidebar.error("""
                **Common issues:**
                - Service account key has expired (generate a new one)
                - Project not registered with Earth Engine
                - Invalid JSON file format
                - Missing required permissions
                
                Check the console logs for detailed error messages.
                """)
                
        except Exception as e:
            st.sidebar.error(f"❌ Error processing credentials: {str(e)}")

# Map Mode Selection
st.sidebar.markdown("### 🌍 **MAP VIEW MODE**")
map_mode = st.sidebar.radio(
    "Choose map display:",
    ["🌐 3D Interactive Globe", "🗺️ 2D Map View"],
    index=0 if st.session_state.map_mode == "globe" else 1,
    help="Switch between 3D interactive globe and 2D map views"
)

# Update session state
st.session_state.map_mode = "globe" if map_mode.startswith("🌐") else "2d"

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
    
    # Professional Study Area Selection
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1a1a1a, #2a2a2a); padding: 15px; border-radius: 10px; border-left: 4px solid #00ff88; margin: 20px 0;">
        <h3 style="color: #00ff88; margin: 0;">📍 TRADING AREA SELECTION</h3>
        <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 0.9rem;">Select your geographical trading zone for vegetation indices analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Country selection
        try:
            countries_fc = get_admin_boundaries(0)
            if countries_fc is not None:
                country_names = get_boundary_names(countries_fc, 0)
                selected_country = st.selectbox(
                    "Select Country",
                    options=[""] + country_names,
                    help="Choose a country for analysis"
                )
            else:
                st.error("Failed to load countries data")
                selected_country = ""
        except Exception as e:
            st.error(f"Error loading countries: {str(e)}")
            selected_country = ""
    
    with col2:
        # Admin1 selection (states/provinces)
        selected_admin1 = ""
        if selected_country and countries_fc is not None:
            try:
                # Get country code
                country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first()
                country_code = country_feature.get('ADM0_CODE').getInfo()
                
                admin1_fc = get_admin_boundaries(1, country_code)
                if admin1_fc is not None:
                    admin1_names = get_boundary_names(admin1_fc, 1)
                    selected_admin1 = st.selectbox(
                        "Select State/Province",
                        options=[""] + admin1_names,
                        help="Choose a state or province"
                    )
                else:
                    st.error("Failed to load admin1 data")
            except Exception as e:
                st.error(f"Error loading admin1: {str(e)}")
    
    with col3:
        # Admin2 selection (municipalities)
        selected_admin2 = ""
        if selected_admin1 and 'admin1_fc' in locals() and admin1_fc is not None:
            try:
                # Get admin1 code
                admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
                admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                
                admin2_fc = get_admin_boundaries(2, None, admin1_code)
                if admin2_fc is not None:
                    admin2_names = get_boundary_names(admin2_fc, 2)
                    selected_admin2 = st.selectbox(
                        "Select Municipality",
                        options=[""] + admin2_names,
                        help="Choose a municipality"
                    )
                else:
                    st.error("Failed to load admin2 data")
            except Exception as e:
                st.error(f"Error loading admin2: {str(e)}")
    
    # Professional GIS Map Display
    if selected_country:
        st.markdown("### 🌍 **KHISBA GIS ANALYTICS WORKSPACE**")
        
        # Map mode indicator
        map_mode_display = "🌐 3D INTERACTIVE GLOBE" if st.session_state.map_mode == "globe" else "🗺️ 2D MAP VIEW"
        st.markdown(f"""
        <div style="text-align: center; background: linear-gradient(90deg, #1a1a2a, #2a1a3a); padding: 10px; border-radius: 5px; margin: 10px 0; border: 2px solid #00ff88;">
            <strong style="color: #00ff88;">{map_mode_display}</strong> • <span style="color: #cccccc;">{"Drag to rotate globe | Scroll to zoom" if st.session_state.map_mode == "globe" else "Drag to pan | Scroll to zoom"}</span>
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
            
            if st.session_state.map_mode == "globe":
                # Create 3D Interactive Globe using Geemap
                st.markdown("""
                <div style="border: 3px solid #00ff88; border-radius: 15px; padding: 5px; background: linear-gradient(45deg, #0a0a0a, #1a1a2a); box-shadow: 0 10px 25px rgba(0, 255, 136, 0.2); margin-bottom: 20px;">
                """, unsafe_allow_html=True)
                
                try:
                    import geemap
                    import geemap.foliumap as geemap
                    
                    # Create geemap with 3D globe
                    Map = geemap.Map(center=[center_lat, center_lon], zoom=4)
                    
                    # Add Earth Engine layers to the globe
                    
                    # 1. Add Sentinel-2 imagery
                    try:
                        # Get recent Sentinel-2 image
                        sentinel = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                            .filterDate('2023-06-01', '2023-09-01') \
                            .filterBounds(geometry) \
                            .median() \
                            .clip(geometry)
                        
                        # Add RGB visualization
                        vis_params = {
                            'min': 0,
                            'max': 3000,
                            'bands': ['B4', 'B3', 'B2']
                        }
                        
                        Map.addLayer(sentinel, vis_params, 'Sentinel-2 Satellite', True, 0.7)
                    except Exception as e:
                        st.warning(f"Could not load Sentinel-2: {str(e)}")
                    
                    # 2. Add NDVI layer
                    try:
                        ndvi = sentinel.normalizedDifference(['B8', 'B4']).rename('NDVI')
                        ndvi_params = {
                            'min': -1,
                            'max': 1,
                            'palette': ['blue', 'white', 'green']
                        }
                        Map.addLayer(ndvi, ndvi_params, 'NDVI Vegetation Index', False, 0.6)
                    except:
                        pass
                    
                    # 3. Add NASA Blue Marble for beautiful globe view
                    try:
                        nasa = ee.Image('NASA/BlueMarble_NextGeneration/v2.1').select(['Red', 'Green', 'Blue'])
                        Map.addLayer(nasa, {'min': 0, 'max': 255}, 'NASA Blue Marble', True, 1.0)
                    except:
                        pass
                    
                    # 4. Add study area boundary
                    Map.addLayer(geometry.style(**{'color': '#00ff88', 'fillColor': '#00ff8822'}), {}, 'Study Area', True)
                    
                    # Add layer control
                    Map.addLayerControl()
                    
                    # Try to set to 3D globe mode
                    try:
                        # For newer geemap versions with globe support
                        Map.setOptions('SATELLITE')
                        # Add terrain if available
                        Map.add_basemap('Esri.WorldTerrain')
                    except:
                        # Fallback to regular view
                        pass
                    
                    # Display the map
                    Map.to_streamlit(height=550)
                    
                except ImportError:
                    st.error("""
                    **Geemap is not installed!**
                    
                    Please install geemap by running:
                    ```bash
                    pip install geemap
                    ```
                    
                    Or for now, using the 2D map view instead.
                    """)
                    
                    # Fallback to 2D map
                    m = folium.Map(
                        location=[center_lat, center_lon],
                        zoom_start=6,
                        tiles=None,
                        control_scale=True,
                        prefer_canvas=True
                    )
                    
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
                    
                    folium.LayerControl().add_to(m)
                    
                    st_folium(m, width=None, height=550)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Globe controls info
                st.markdown("""
                <div style="background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #00ff88;">
                    <h4 style="color: #00ff88; margin-top: 0;">🎮 Earth Engine Globe Controls:</h4>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px;">
                        <div>
                            <strong style="color: #ffffff;">🛰️ Satellite Layers:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>Sentinel-2:</strong> High-res satellite imagery<br>
                            • <strong>NASA Blue Marble:</strong> Global Earth view<br>
                            • <strong>NDVI:</strong> Vegetation health index<br>
                            • <strong>Study Area:</strong> Green highlighted region
                            </span>
                        </div>
                        <div>
                            <strong style="color: #ffffff;">🎯 Navigation:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>Layers:</strong> Toggle visibility in top-right<br>
                            • <strong>Drag:</strong> Pan/rotate view<br>
                            • <strong>Scroll:</strong> Zoom in/out<br>
                            • <strong>Search:</strong> Find locations
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                # Create 2D professional GIS map (original code)
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=6,
                    tiles=None,
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
                    st.markdown("""
                    <div style="border: 3px solid #00ff88; border-radius: 10px; padding: 5px; background: linear-gradient(45deg, #0a0a0a, #1a1a1a);">
                    """, unsafe_allow_html=True)
                    
                    map_data = st_folium(
                        m, 
                        width=None, 
                        height=500,
                        returned_objects=["last_clicked", "bounds", "zoom"],
                        key="gis_map_2d"
                    )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Professional GIS information panel
            if st.session_state.map_mode == "globe":
                col1, col2 = st.columns([1, 1])
                with col2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a2a, #2a2a3a); padding: 20px; border-radius: 15px; border: 2px solid #00ff88; box-shadow: 0 8px 25px rgba(0, 255, 136, 0.15); margin-top: 20px;">
                        <h4 style="color: #00ff88; margin-top: 0; text-align: center;">🌍 EARTH ENGINE GLOBE</h4>
                        <div style="text-align: center; margin-bottom: 15px;">
                            <span style="background: #00ff88; color: #000000; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">REAL-TIME SATELLITE DATA</span>
                        </div>
                        <hr style="border-color: #00ff88;">
                        
                        <div style="margin: 15px 0;">
                            <strong style="color: #ffffff;">📌 Study Area:</strong><br>
                            <span style="color: #cccccc;">{area_name}</span>
                        </div>
                        
                        <div style="margin: 15px 0;">
                            <strong style="color: #ffffff;">📊 Administrative Level:</strong><br>
                            <span style="color: #00ff88;">{area_level}</span>
                        </div>
                        
                        <div style="margin: 15px 0;">
                            <strong style="color: #ffffff;">📍 Coordinates:</strong><br>
                            <span style="color: #cccccc; font-family: monospace;">Lat: {center_lat:.4f}°<br>
                            Lon: {center_lon:.4f}°</span>
                        </div>
                        
                        <div style="margin: 15px 0;">
                            <strong style="color: #ffffff;">🛰️ Active Layers:</strong><br>
                            <span style="color: #00ff88;">Sentinel-2 • NASA • NDVI</span>
                        </div>
                        
                        <div style="background: rgba(0, 255, 136, 0.1); padding: 12px; border-radius: 8px; margin-top: 20px; border-left: 3px solid #00ff88;">
                            <small style="color: #00ff88; display: block; margin-bottom: 5px;">💡 Pro Tip:</small>
                            <small style="color: #888888; font-size: 0.85em;">
                            • Toggle layers in top-right control<br>
                            • <span style="color: #00ff88;">NDVI layer</span> shows vegetation health<br>
                            • Use search to find any location
                            </small>
                        </div>
                        
                        <div style="background: #0a0a0a; padding: 10px; border-radius: 5px; margin-top: 20px; text-align: center;">
                            <small style="color: #00ff88;">📊 KHISBA GIS Professional</small><br>
                            <small style="color: #888888;">Powered by Google Earth Engine</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                col1, col2 = st.columns([2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 20px; border-radius: 10px; border: 1px solid #00ff88;">
                        <h4 style="color: #00ff88; margin-top: 0;">🌍 GIS DATA PANEL</h4>
                        <hr style="border-color: #00ff88;">
                        
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
                        
                        <div style="background: #0a0a0a; padding: 10px; border-radius: 5px; margin-top: 20px;">
                            <small style="color: #00ff88;">📊 KHISBA GIS Professional</small><br>
                            <small style="color: #888888;">Powered by Earth Engine</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.session_state.selected_geometry = geometry
            
            # Professional status indicator
            status_icon = "🌐" if st.session_state.map_mode == "globe" else "🗺️"
            st.markdown(f"""
            <div style="text-align: center; background: linear-gradient(90deg, #00ff88, #004422); padding: 12px; border-radius: 8px; margin: 15px 0; border: 1px solid #ffffff;">
                <strong style="color: white; font-size: 1.1em;">✅ GIS WORKSPACE ACTIVE</strong><br>
                <span style="color: #e8f5e8; font-size: 0.9em;">{status_icon} {area_name} • {area_level} • {map_mode_display}</span>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ GIS Map Error: {str(e)}")
            st.info("Please check your internet connection and try refreshing the page.")
    
    # Professional Analysis Parameters
    if st.session_state.selected_geometry is not None:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #2a1a1a, #3a2a1a); padding: 15px; border-radius: 10px; border-left: 4px solid #ffaa00; margin: 20px 0;">
            <h3 style="color: #ffaa00; margin: 0;">⚙️ TRADING PARAMETERS</h3>
            <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 0.9rem;">Configure your analysis timeframe and satellite data sources</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime(2023, 1, 1),
                help="Start date for the analysis period"
            )
            
            cloud_cover = st.slider(
                "Maximum Cloud Cover (%)",
                min_value=0,
                max_value=100,
                value=20,
                help="Maximum cloud cover percentage for images"
            )
        
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime(2023, 12, 31),
                help="End date for the analysis period"
            )
            
            collection_choice = st.selectbox(
                "Satellite Collection",
                options=["Sentinel-2", "Landsat-8"],
                help="Choose the satellite collection for analysis"
            )
        
        # Vegetation Indices Selection
        st.subheader("🌿 Vegetation Indices Selection")
        
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
        
        # Run Analysis Button
        if st.button("🚀 Run Analysis", type="primary"):
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

# Display Results
if st.session_state.analysis_results:
    st.header("📊 Analysis Results")
    
    results = st.session_state.analysis_results
    
    # Summary statistics
    st.subheader("📈 Summary Statistics")
    
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
    
    # Professional Analytics Charts
    st.markdown("### 📈 **PROFESSIONAL VEGETATION ANALYTICS**")
    
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
                            <div style="text-align: center; background: #1a1a1a; padding: 10px; border-radius: 10px; margin: 10px 0;">
                                <h4 style="color: {change_color}; margin: 0;">{change_symbol} {index} INDEX</h4>
                                <h2 style="color: white; margin: 5px 0;">{current_value:.4f}</h2>
                                <p style="color: {change_color}; margin: 0; font-size: 14px;">{change_pct:+.2f}% • {trend_text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.plotly_chart(fig, width='stretch')
                        
                except Exception as e:
                    st.error(f"Error creating chart for {index}: {str(e)}")
    
    # Data Export
    st.subheader("💾 Data Export")
    
    if st.button("📥 Download Results as CSV"):
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
        st.info("👆 Earth Engine is initializing... Please wait or upload credentials if needed")
    elif st.session_state.selected_geometry is None:
        st.info("👆 Please select a study area to proceed with analysis")
    else:
        st.info("👆 Configure your analysis parameters and click 'Run Analysis'")
