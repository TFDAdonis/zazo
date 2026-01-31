import streamlit as st
import json
import tempfile
import os
import pandas as pd
import folium
from streamlit_folium import st_folium
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
if 'map_view' not in st.session_state:
    st.session_state.map_view = "2d"  # Default to 2D view
if 'current_zoom' not in st.session_state:
    st.session_state.current_zoom = 6
if 'globe_rotation' not in st.session_state:
    st.session_state.globe_rotation = {'lat': 0, 'lon': 0}

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

# Map View Toggle in Sidebar
st.sidebar.markdown("### 🌍 **MAP VIEW MODE**")
map_view = st.sidebar.radio(
    "Select Map View:",
    ["🗺️ 2D Interactive Map", "🌐 3D Interactive Globe"],
    index=0 if st.session_state.map_view == "2d" else 1,
    help="Switch between 2D map and 3D globe views"
)

# Update session state
st.session_state.map_view = "2d" if map_view.startswith("🗺️") else "3d"

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
        
        # Map view indicator
        view_mode = "🗺️ 2D INTERACTIVE MAP" if st.session_state.map_view == "2d" else "🌐 3D INTERACTIVE GLOBE"
        st.markdown(f"""
        <div style="text-align: center; background: linear-gradient(90deg, #1a1a2a, #2a1a3a); padding: 10px; border-radius: 5px; margin: 10px 0; border: 2px solid #00ff88;">
            <strong style="color: #00ff88;">{view_mode}</strong> • <span style="color: #cccccc;">{"Drag to pan | Scroll to zoom" if st.session_state.map_view == "2d" else "Drag to rotate globe | Scroll to zoom"}</span>
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
            
            if st.session_state.map_view == "2d":
                # Create 2D Interactive Map with Folium
                st.markdown("""
                <div style="border: 3px solid #00ff88; border-radius: 15px; padding: 5px; background: linear-gradient(45deg, #0a0a0a, #1a1a2a); box-shadow: 0 10px 25px rgba(0, 255, 136, 0.2); margin-bottom: 20px;">
                """, unsafe_allow_html=True)
                
                # Create a beautiful interactive 2D map
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=st.session_state.current_zoom,
                    tiles=None,
                    control_scale=True,
                    prefer_canvas=True,
                    max_bounds=True,
                    max_lat=85,
                    min_lat=-85
                )
                
                # Add multiple base layers
                
                # OpenStreetMap (always works)
                folium.TileLayer(
                    'OpenStreetMap',
                    name='🗺️ Street Map',
                    attr='OpenStreetMap contributors',
                    overlay=False,
                    control=True
                ).add_to(m)
                
                # CartoDB Dark Matter
                folium.TileLayer(
                    'CartoDB dark_matter',
                    name='🌑 Dark Theme',
                    attr='CartoDB',
                    overlay=False,
                    control=True
                ).add_to(m)
                
                # CartoDB Positron
                folium.TileLayer(
                    'CartoDB positron',
                    name='☀️ Light Theme',
                    attr='CartoDB',
                    overlay=False,
                    control=True
                ).add_to(m)
                
                # Stamen Terrain
                folium.TileLayer(
                    'Stamen Terrain',
                    name='🏔️ Terrain',
                    attr='Stamen',
                    overlay=False,
                    control=True
                ).add_to(m)
                
                # Try ESRI Satellite
                try:
                    folium.TileLayer(
                        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                        name='🛰️ Satellite',
                        attr='Esri',
                        overlay=False,
                        control=True
                    ).add_to(m)
                except:
                    pass
                
                # Add study area with glowing effect
                study_area_style = {
                    'fillColor': '#00ff88',
                    'color': '#ffffff',
                    'weight': 4,
                    'fillOpacity': 0.3,
                    'dashArray': '5, 5',
                    'opacity': 0.8
                }
                
                # Add GeoJson with popup
                folium.GeoJson(
                    bounds,
                    style_function=lambda x: study_area_style,
                    popup=folium.Popup(
                        f"""
                        <div style="font-family: Arial, sans-serif; padding: 10px;">
                            <h3 style="color: #00ff88; margin-top: 0;">📌 STUDY AREA</h3>
                            <hr style="border-color: #00ff88;">
                            <p><strong>📍 Location:</strong> {area_name}</p>
                            <p><strong>📊 Level:</strong> {area_level}</p>
                            <p><strong>🌐 Coordinates:</strong><br>
                            Lat: {center_lat:.4f}°<br>
                            Lon: {center_lon:.4f}°</p>
                            <p><strong>🔍 Status:</strong> Active for analysis</p>
                            <div style="background: #1a1a1a; padding: 8px; border-radius: 5px; margin-top: 10px;">
                                <small style="color: #00ff88;">KHISBA GIS Professional</small>
                            </div>
                        </div>
                        """, 
                        max_width=350
                    ),
                    tooltip=f"📍 {area_name} | Click for details"
                ).add_to(m)
                
                # Add a marker at the center
                folium.CircleMarker(
                    location=[center_lat, center_lon],
                    radius=10,
                    popup=f"Center: {center_lat:.4f}, {center_lon:.4f}",
                    color='#00ff88',
                    fill=True,
                    fillColor='#00ff88',
                    fillOpacity=0.7,
                    weight=3
                ).add_to(m)
                
                # Add plugins
                from folium.plugins import MousePosition, MeasureControl, Fullscreen, MiniMap
                
                # Mouse position
                MousePosition(
                    position='bottomleft',
                    separator=' | ',
                    empty_string='Drag map to explore',
                    lng_first=True,
                    num_digits=4,
                    prefix='Coordinates:',
                    lat_formatter=lambda x: f'Lat: {x:.4f}°',
                    lng_formatter=lambda x: f'Lon: {x:.4f}°'
                ).add_to(m)
                
                # Measurement tool
                MeasureControl(
                    position='bottomleft',
                    primary_length_unit='kilometers',
                    secondary_length_unit='miles',
                    primary_area_unit='sqkilometers',
                    secondary_area_unit='acres'
                ).add_to(m)
                
                # Fullscreen mode
                Fullscreen(
                    position='topright',
                    title='Expand me',
                    title_cancel='Exit fullscreen',
                    force_separate_button=True
                ).add_to(m)
                
                # Mini map
                minimap = MiniMap(
                    tile_layer='CartoDB dark_matter',
                    position='bottomright',
                    width=150,
                    height=150,
                    zoom_level_offset=-5,
                    toggle_display=True
                )
                m.add_child(minimap)
                
                # Add layer control
                folium.LayerControl(
                    position='topright',
                    collapsed=True
                ).add_to(m)
                
                # Display the map
                map_data = st_folium(
                    m, 
                    width=None, 
                    height=600,
                    returned_objects=["last_clicked", "bounds", "zoom"],
                    key="2d_map"
                )
                
                # Update zoom state
                if map_data and 'zoom' in map_data and map_data['zoom'] is not None:
                    st.session_state.current_zoom = map_data['zoom']
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            else:
                # Create 3D Interactive Globe with Plotly
                st.markdown("""
                <div style="border: 3px solid #00ff88; border-radius: 15px; padding: 5px; background: linear-gradient(45deg, #0a0a0a, #1a1a2a); box-shadow: 0 10px 25px rgba(0, 255, 136, 0.2); margin-bottom: 20px;">
                """, unsafe_allow_html=True)
                
                # Layer selection for 3D globe
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 🌍 **3D GLOBE LAYERS**")
                    show_country_borders = st.checkbox("Country Borders", value=True)
                    show_terrain = st.checkbox("Terrain Elevation", value=True)
                    show_satellite = st.checkbox("Satellite Imagery", value=True)
                    show_streets = st.checkbox("Street Map Overlay", value=False)
                    show_cities = st.checkbox("Major Cities", value=True)
                    show_clouds = st.checkbox("Cloud Cover", value=False)
                
                with col2:
                    st.markdown("### 🎨 **VISUALIZATION SETTINGS**")
                    globe_opacity = st.slider("Globe Opacity", 0.5, 1.0, 0.9, 0.05)
                    layer_opacity = st.slider("Layer Opacity", 0.3, 1.0, 0.7, 0.05)
                    elevation_scale = st.slider("Terrain Scale", 0.5, 3.0, 1.5, 0.1)
                
                # Create 3D globe
                fig = go.Figure()
                
                # Create sphere coordinates
                u = np.linspace(0, 2 * np.pi, 100)
                v = np.linspace(0, np.pi, 50)
                u, v = np.meshgrid(u, v)
                
                r = 1.0  # Earth radius
                x = r * np.sin(v) * np.cos(u)
                y = r * np.sin(v) * np.sin(u)
                z = r * np.cos(v)
                
                # Base Earth texture - choose between different base layers
                if show_satellite:
                    # Satellite imagery texture (simulated with gradient)
                    colorscale = [
                        [0, '#0a2f5a'],      # Deep ocean
                        [0.2, '#1a5f7a'],    # Ocean
                        [0.4, '#2a8bb9'],    # Shallow water
                        [0.5, '#57a7d4'],    # Coast
                        [0.6, '#7dc8c8'],    # Coastal areas
                        [0.65, '#a8d5ba'],   # Lowlands
                        [0.75, '#8fbc8f'],   # Vegetation
                        [0.85, '#b8860b'],   # Mountains
                        [0.95, '#8b7355'],   # High mountains
                        [1.0, '#6b5b45']     # Snow caps
                    ]
                    base_name = "Satellite Imagery"
                elif show_streets:
                    # Street map style (simplified)
                    colorscale = [
                        [0, '#1a5f7a'],      # Water
                        [0.3, '#57a7d4'],    # Shallow water
                        [0.4, '#d4e6f1'],    # Land
                        [0.6, '#f5f5dc'],    # Urban areas
                        [0.8, '#d3d3d3'],    # Roads/streets
                        [1.0, '#a9a9a9']     # Major highways
                    ]
                    base_name = "Street Map"
                else:
                    # Physical map style
                    colorscale = [
                        [0, '#1a5f7a'],      # Deep ocean
                        [0.2, '#2a8bb9'],    # Ocean
                        [0.4, '#57a7d4'],    # Shallow water
                        [0.6, '#89c2d9'],    # Coast
                        [0.7, '#a8d5ba'],    # Lowlands
                        [0.8, '#8fbc8f'],    # Vegetation
                        [0.9, '#b8860b'],    # Mountains
                        [1.0, '#8b7355']     # High mountains
                    ]
                    base_name = "Physical Map"
                
                # Add base Earth surface
                fig.add_trace(go.Surface(
                    x=x, y=y, z=z,
                    colorscale=colorscale,
                    showscale=False,
                    opacity=globe_opacity,
                    lighting=dict(
                        ambient=0.7,
                        diffuse=0.9,
                        roughness=0.8,
                        specular=0.9
                    ),
                    lightposition=dict(x=10000, y=10000, z=10000),
                    name=base_name
                ))
                
                # Add terrain elevation layer (applies to all base maps)
                if show_terrain:
                    # Create exaggerated terrain effect
                    terrain_r = r * (1 + 0.015 * np.sin(8*u) * np.sin(4*v) * elevation_scale)
                    terrain_x = terrain_r * np.sin(v) * np.cos(u)
                    terrain_y = terrain_r * np.sin(v) * np.sin(u)
                    terrain_z = terrain_r * np.cos(v)
                    
                    # Adjust terrain colors based on base map
                    if show_satellite:
                        terrain_colorscale = [
                            [0, 'rgba(139, 115, 85, 0.4)'],   # Mountains
                            [0.5, 'rgba(184, 134, 11, 0.5)'], # Highlands
                            [1, 'rgba(143, 188, 143, 0.6)']   # Lowlands
                        ]
                    elif show_streets:
                        terrain_colorscale = [
                            [0, 'rgba(169, 169, 169, 0.3)'],  # Urban relief
                            [1, 'rgba(211, 211, 211, 0.5)']   # Suburban relief
                        ]
                    else:
                        terrain_colorscale = [
                            [0, 'rgba(139, 115, 85, 0.3)'],   # Mountains
                            [0.5, 'rgba(184, 134, 11, 0.4)'], # Highlands
                            [1, 'rgba(143, 188, 143, 0.5)']   # Lowlands
                        ]
                    
                    fig.add_trace(go.Surface(
                        x=terrain_x, y=terrain_y, z=terrain_z,
                        colorscale=terrain_colorscale,
                        showscale=False,
                        opacity=layer_opacity * 0.5,
                        name="Terrain Elevation"
                    ))
                
                # Add country borders layer with proper political boundaries
                if show_country_borders:
                    try:
                        # Get country boundaries from Earth Engine
                        countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
                        
                        # Get a few sample countries for demonstration
                        sample_countries = ['United States', 'Canada', 'Mexico', 'Brazil', 'Argentina', 
                                          'France', 'Germany', 'Italy', 'Spain', 'United Kingdom',
                                          'China', 'India', 'Russia', 'Australia', 'South Africa']
                        
                        for country_name in sample_countries:
                            try:
                                country = countries.filter(ee.Filter.eq('country_na', country_name)).first()
                                geometry = country.geometry()
                                
                                # Get coordinates
                                coords = geometry.coordinates().getInfo()
                                
                                # Process coordinates based on geometry type
                                if isinstance(coords[0][0], list):  # Polygon
                                    rings = coords
                                elif isinstance(coords[0][0][0], list):  # MultiPolygon
                                    rings = []
                                    for polygon in coords:
                                        rings.extend(polygon)
                                else:
                                    continue
                                
                                # Plot each ring
                                for ring in rings:
                                    lons = [coord[0] for coord in ring]
                                    lats = [coord[1] for coord in ring]
                                    
                                    # Convert to 3D coordinates
                                    lat_rad = np.radians(np.array(lats))
                                    lon_rad = np.radians(np.array(lons))
                                    
                                    border_x = r * np.cos(lat_rad) * np.cos(lon_rad)
                                    border_y = r * np.cos(lat_rad) * np.sin(lon_rad)
                                    border_z = r * np.sin(lat_rad)
                                    
                                    # Use different colors for different continents
                                    if country_name in ['United States', 'Canada', 'Mexico', 'Brazil', 'Argentina']:
                                        border_color = 'rgba(255, 100, 100, 0.8)'  # Americas - Red
                                    elif country_name in ['France', 'Germany', 'Italy', 'Spain', 'United Kingdom']:
                                        border_color = 'rgba(100, 255, 100, 0.8)'  # Europe - Green
                                    elif country_name in ['China', 'India', 'Russia']:
                                        border_color = 'rgba(100, 100, 255, 0.8)'  # Asia - Blue
                                    else:
                                        border_color = 'rgba(255, 255, 100, 0.8)'  # Others - Yellow
                                    
                                    fig.add_trace(go.Scatter3d(
                                        x=border_x, y=border_y, z=border_z,
                                        mode='lines',
                                        line=dict(color=border_color, width=1.5),
                                        showlegend=False,
                                        hoverinfo='skip',
                                        name=f"{country_name} Border"
                                    ))
                                    
                            except Exception as e:
                                continue
                        
                        # Add a legend entry for borders
                        fig.add_trace(go.Scatter3d(
                            x=[None], y=[None], z=[None],
                            mode='markers',
                            marker=dict(size=0),
                            line=dict(color='rgba(255, 100, 100, 0.8)', width=2),
                            name="Country Borders",
                            showlegend=True
                        ))
                                
                    except Exception as e:
                        # Fallback: Add simplified continental borders
                        st.sidebar.warning(f"Detailed country borders loading limited. Using continental borders instead.")
                        
                        # Continental boundaries (simplified)
                        continents = [
                            {'name': 'North America', 'lat_range': (15, 70), 'lon_range': (-170, -50), 'color': 'rgba(255, 100, 100, 0.8)'},
                            {'name': 'South America', 'lat_range': (-55, 15), 'lon_range': (-85, -30), 'color': 'rgba(255, 150, 100, 0.8)'},
                            {'name': 'Europe', 'lat_range': (35, 70), 'lon_range': (-10, 60), 'color': 'rgba(100, 255, 100, 0.8)'},
                            {'name': 'Africa', 'lat_range': (-35, 37), 'lon_range': (-20, 50), 'color': 'rgba(255, 255, 100, 0.8)'},
                            {'name': 'Asia', 'lat_range': (10, 70), 'lon_range': (60, 180), 'color': 'rgba(100, 100, 255, 0.8)'},
                            {'name': 'Australia', 'lat_range': (-45, -10), 'lon_range': (110, 180), 'color': 'rgba(255, 100, 255, 0.8)'}
                        ]
                        
                        for continent in continents:
                            # Create a simple rectangular border for each continent
                            lat_min, lat_max = continent['lat_range']
                            lon_min, lon_max = continent['lon_range']
                            
                            # Create border points (rectangle)
                            border_lats = [lat_min, lat_max, lat_max, lat_min, lat_min]
                            border_lons = [lon_min, lon_min, lon_max, lon_max, lon_min]
                            
                            # Convert to 3D
                            lat_rad = np.radians(np.array(border_lats))
                            lon_rad = np.radians(np.array(border_lons))
                            
                            border_x = r * np.cos(lat_rad) * np.cos(lon_rad)
                            border_y = r * np.cos(lat_rad) * np.sin(lon_rad)
                            border_z = r * np.sin(lat_rad)
                            
                            fig.add_trace(go.Scatter3d(
                                x=border_x, y=border_y, z=border_z,
                                mode='lines',
                                line=dict(color=continent['color'], width=1.5),
                                showlegend=True,
                                name=f"{continent['name']} Border",
                                hoverinfo='skip'
                            ))
                
                # Add major cities layer
                if show_cities:
                    # Sample major cities with their coordinates
                    major_cities = [
                        {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503, 'pop': '37M', 'country': 'Japan'},
                        {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'pop': '18M', 'country': 'USA'},
                        {'name': 'London', 'lat': 51.5074, 'lon': -0.1278, 'pop': '9M', 'country': 'UK'},
                        {'name': 'Paris', 'lat': 48.8566, 'lon': 2.3522, 'pop': '11M', 'country': 'France'},
                        {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'pop': '5M', 'country': 'Australia'},
                        {'name': 'Dubai', 'lat': 25.2048, 'lon': 55.2708, 'pop': '3M', 'country': 'UAE'},
                        {'name': 'Singapore', 'lat': 1.3521, 'lon': 103.8198, 'pop': '6M', 'country': 'Singapore'},
                        {'name': 'Cairo', 'lat': 30.0444, 'lon': 31.2357, 'pop': '20M', 'country': 'Egypt'},
                        {'name': 'Moscow', 'lat': 55.7558, 'lon': 37.6173, 'pop': '12M', 'country': 'Russia'},
                        {'name': 'Rio', 'lat': -22.9068, 'lon': -43.1729, 'pop': '13M', 'country': 'Brazil'},
                        {'name': 'Beijing', 'lat': 39.9042, 'lon': 116.4074, 'pop': '21M', 'country': 'China'},
                        {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'pop': '20M', 'country': 'India'}
                    ]
                    
                    city_x = []
                    city_y = []
                    city_z = []
                    city_names = []
                    city_info = []
                    
                    for city in major_cities:
                        lat_rad = np.radians(city['lat'])
                        lon_rad = np.radians(city['lon'])
                        
                        city_x.append(r * np.cos(lat_rad) * np.cos(lon_rad))
                        city_y.append(r * np.cos(lat_rad) * np.sin(lon_rad))
                        city_z.append(r * np.sin(lat_rad))
                        city_names.append(city['name'])
                        city_info.append(f"{city['name']}, {city['country']}<br>Population: {city['pop']}")
                    
                    # City markers with size based on population
                    marker_sizes = [8 if 'M' in city['pop'] and int(city['pop'].replace('M', '')) > 10 else 6 for city in major_cities]
                    
                    fig.add_trace(go.Scatter3d(
                        x=city_x, y=city_y, z=city_z,
                        mode='markers',
                        marker=dict(
                            size=marker_sizes,
                            color='#FF6B6B',
                            symbol='circle',
                            line=dict(color='white', width=1)
                        ),
                        text=city_names,
                        hovertemplate='<b>%{text}</b><br>%{customdata}<extra></extra>',
                        customdata=city_info,
                        name="Major Cities"
                    ))
                
                # Add street grid overlay (for street map view)
                if show_streets:
                    # Add a grid pattern to simulate streets
                    street_r = r * 1.001
                    
                    # Create grid pattern
                    grid_size = 20
                    for i in range(grid_size):
                        lon = i * (360/grid_size)
                        lon_rad = np.radians(lon)
                        lat_points = np.linspace(-np.pi/2 + 0.1, np.pi/2 - 0.1, 50)
                        
                        # Vertical lines (longitude)
                        x_line = street_r * np.cos(lat_points) * np.cos(lon_rad)
                        y_line = street_r * np.cos(lat_points) * np.sin(lon_rad)
                        z_line = street_r * np.sin(lat_points)
                        
                        fig.add_trace(go.Scatter3d(
                            x=x_line, y=y_line, z=z_line,
                            mode='lines',
                            line=dict(color='rgba(100, 100, 100, 0.3)', width=0.5),
                            showlegend=False,
                            hoverinfo='skip',
                            name="Street Grid"
                        ))
                    
                    # Add major highways (thicker lines at specific longitudes)
                    major_highways = [0, 90, 180, 270]  # Prime meridian, 90°E, 180°, 90°W
                    for lon in major_highways:
                        lon_rad = np.radians(lon)
                        lat_points = np.linspace(-np.pi/2 + 0.1, np.pi/2 - 0.1, 100)
                        
                        x_line = street_r * np.cos(lat_points) * np.cos(lon_rad)
                        y_line = street_r * np.cos(lat_points) * np.sin(lon_rad)
                        z_line = street_r * np.sin(lat_points)
                        
                        fig.add_trace(go.Scatter3d(
                            x=x_line, y=y_line, z=z_line,
                            mode='lines',
                            line=dict(color='rgba(255, 100, 100, 0.5)', width=1.5),
                            showlegend=False,
                            hoverinfo='skip',
                            name="Major Highways"
                        ))
                
                # Add cloud cover layer
                if show_clouds:
                    cloud_r = r * 1.005
                    
                    # Create cloud-like pattern using multiple sine waves
                    cloud_pattern = (0.5 + 0.3 * np.sin(15*u) * np.cos(8*v) * 
                                    np.sin(3*u + 2*v) * np.cos(5*u - 3*v))
                    
                    # Add some randomness
                    cloud_pattern += 0.1 * np.random.randn(*u.shape)
                    
                    fig.add_trace(go.Surface(
                        x=cloud_r * np.sin(v) * np.cos(u),
                        y=cloud_r * np.sin(v) * np.sin(u),
                        z=cloud_r * np.cos(v) + 0.01 * cloud_pattern,
                        colorscale=[[0, 'rgba(255, 255, 255, 0.1)'], [1, 'rgba(255, 255, 255, 0.3)']],
                        showscale=False,
                        opacity=layer_opacity * 0.3,
                        name="Cloud Cover"
                    ))
                
                # Add atmosphere glow
                fig.add_trace(go.Surface(
                    x=x*1.02, y=y*1.02, z=z*1.02,
                    colorscale=[[0, 'rgba(135, 206, 235, 0.1)'], [1, 'rgba(135, 206, 235, 0.05)']],
                    showscale=False,
                    opacity=0.3,
                    name="Atmosphere"
                ))
                
                # Add study area marker
                lat_rad = np.radians(center_lat)
                lon_rad = np.radians(center_lon)
                
                marker_x = r * np.cos(lat_rad) * np.cos(lon_rad)
                marker_y = r * np.cos(lat_rad) * np.sin(lon_rad)
                marker_z = r * np.sin(lat_rad)
                
                fig.add_trace(go.Scatter3d(
                    x=[marker_x],
                    y=[marker_y],
                    z=[marker_z],
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color='#00ff88',
                        symbol='circle',
                        line=dict(color='white', width=3)
                    ),
                    text=["📍"],
                    textposition="top center",
                    textfont=dict(size=25, color='#00ff88'),
                    name=f"📍 Study Area: {area_name}",
                    hovertemplate=f"""
                    <b>📍 Study Area:</b> {area_name}<br>
                    <b>📊 Level:</b> {area_level}<br>
                    <b>🌐 Coordinates:</b> {center_lat:.4f}°N, {center_lon:.4f}°E<br>
                    <b>🔍 Status:</b> Active for analysis
                    <extra></extra>
                    """
                ))
                
                # Add latitude/longitude grid (always visible for reference)
                grid_opacity = 0.15
                
                # Latitude lines
                for lat in range(-80, 81, 20):
                    lat_rad = np.radians(lat)
                    lon_points = np.linspace(0, 2*np.pi, 100)
                    x_lat = r * np.cos(lat_rad) * np.cos(lon_points)
                    y_lat = r * np.cos(lat_rad) * np.sin(lon_points)
                    z_lat = r * np.sin(lat_rad) * np.ones_like(lon_points)
                    
                    fig.add_trace(go.Scatter3d(
                        x=x_lat, y=y_lat, z=z_lat,
                        mode='lines',
                        line=dict(color='rgba(255, 255, 255, 0.2)', width=0.5),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                
                # Longitude lines
                for lon in range(0, 360, 30):
                    lon_rad = np.radians(lon)
                    lat_points = np.linspace(-np.pi/2 + 0.1, np.pi/2 - 0.1, 100)
                    x_lon = r * np.cos(lat_points) * np.cos(lon_rad)
                    y_lon = r * np.cos(lat_points) * np.sin(lon_rad)
                    z_lon = r * np.sin(lat_points)
                    
                    fig.add_trace(go.Scatter3d(
                        x=x_lon, y=y_lon, z=z_lon,
                        mode='lines',
                        line=dict(color='rgba(255, 255, 255, 0.2)', width=0.5),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                
                # Add equator highlight
                equator_lat = 0
                lat_rad = np.radians(equator_lat)
                lon_points = np.linspace(0, 2*np.pi, 200)
                x_eq = r * np.cos(lat_rad) * np.cos(lon_points)
                y_eq = r * np.cos(lat_rad) * np.sin(lon_points)
                z_eq = r * np.sin(lat_rad) * np.ones_like(lon_points)
                
                fig.add_trace(go.Scatter3d(
                    x=x_eq, y=y_eq, z=z_eq,
                    mode='lines',
                    line=dict(color='rgba(255, 100, 100, 0.5)', width=2),
                    showlegend=False,
                    hoverinfo='skip',
                    name="Equator"
                ))
                
                # Add tropics lines
                for tropic_lat in [23.5, -23.5]:  # Tropic of Cancer and Capricorn
                    lat_rad = np.radians(tropic_lat)
                    lon_points = np.linspace(0, 2*np.pi, 200)
                    x_tropic = r * np.cos(lat_rad) * np.cos(lon_points)
                    y_tropic = r * np.cos(lat_rad) * np.sin(lon_points)
                    z_tropic = r * np.sin(lat_rad) * np.ones_like(lon_points)
                    
                    fig.add_trace(go.Scatter3d(
                        x=x_tropic, y=y_tropic, z=z_tropic,
                        mode='lines',
                        line=dict(color='rgba(255, 200, 100, 0.4)', width=1),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                
                # Configure globe layout with enhanced controls
                fig.update_layout(
                    title=dict(
                        text=f"<b>3D Interactive Globe with Multiple Layers</b><br><span style='font-size:14px;color:#cccccc'>📍 {area_name} • Drag to rotate • Scroll to zoom</span>",
                        x=0.5,
                        xanchor='center',
                        font=dict(size=20, color='white')
                    ),
                    scene=dict(
                        xaxis=dict(
                            showbackground=False,
                            showticklabels=False,
                            showgrid=False,
                            zeroline=False,
                            title=''
                        ),
                        yaxis=dict(
                            showbackground=False,
                            showticklabels=False,
                            showgrid=False,
                            zeroline=False,
                            title=''
                        ),
                        zaxis=dict(
                            showbackground=False,
                            showticklabels=False,
                            showgrid=False,
                            zeroline=False,
                            title=''
                        ),
                        aspectmode='data',
                        camera=dict(
                            eye=dict(
                                x=1.5 * np.cos(st.session_state.globe_rotation['lon'] * np.pi/180),
                                y=1.5 * np.sin(st.session_state.globe_rotation['lon'] * np.pi/180),
                                z=1.0 + 0.5 * np.sin(st.session_state.globe_rotation['lat'] * np.pi/180)
                            ),
                            up=dict(x=0, y=0, z=1),
                            center=dict(x=0, y=0, z=0)
                        ),
                        bgcolor='#0a0a0a'
                    ),
                    paper_bgcolor='#0a0a0a',
                    plot_bgcolor='#0a0a0a',
                    font=dict(color='white'),
                    height=600,
                    showlegend=True,
                    legend=dict(
                        x=0.02,
                        y=0.98,
                        bgcolor='rgba(0,0,0,0.7)',
                        bordercolor='#666666',
                        borderwidth=1,
                        font=dict(size=10),
                        itemsizing='constant',
                        itemclick='toggleothers',
                        itemdoubleclick='toggle'
                    ),
                    margin=dict(l=0, r=0, t=80, b=0)
                )
                
                # Display the 3D globe
                st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'scrollZoom': True,
                    'displaylogo': False,
                    'modeBarButtonsToAdd': [
                        'resetCameraDefault3d',
                        'resetCameraLastSave3d',
                        'drawline',
                        'drawopenpath',
                        'drawcircle',
                        'drawrect',
                        'eraseshape'
                    ],
                    'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': 'khisba_3d_globe',
                        'height': 800,
                        'width': 1200,
                        'scale': 2
                    }
                })
                
                # Globe controls
                st.markdown("### 🎮 **3D GLOBE CONTROLS**")
                
                control_cols = st.columns(4)
                
                with control_cols[0]:
                    if st.button("🔄 Reset View", type="secondary", use_container_width=True):
                        st.session_state.globe_rotation = {'lat': 0, 'lon': 0}
                        st.rerun()
                
                with control_cols[1]:
                    if st.button("🎯 Center on Area", type="secondary", use_container_width=True):
                        st.session_state.globe_rotation = {'lat': center_lat, 'lon': center_lon}
                        st.rerun()
                
                with control_cols[2]:
                    if st.button("🌍 Default Map", type="secondary", use_container_width=True):
                        # This would reset to default settings
                        st.info("Default physical map view restored")
                
                with control_cols[3]:
                    if st.button("📸 Screenshot", type="secondary", use_container_width=True):
                        st.info("Right-click on the globe and select 'Save image as...' to save a screenshot")
                
                # Layer status display
                active_layers = [base_name]
                if show_country_borders: active_layers.append("Country Borders")
                if show_terrain: active_layers.append("Terrain")
                if show_cities: active_layers.append("Cities")
                if show_streets: active_layers.append("Street Grid")
                if show_clouds: active_layers.append("Clouds")
                active_layers.append("Lat/Long Grid")
                
                st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #00ff88;">
                    <h4 style="color: #00ff88; margin-top: 0;">📊 ACTIVE LAYERS: {len(active_layers)}</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                        {''.join([f'<span style="background: rgba(0, 255, 136, 0.2); padding: 5px 10px; border-radius: 20px; color: #00ff88; font-size: 0.9em;">{layer}</span>' for layer in active_layers])}
                    </div>
                    <p style="color: #cccccc; margin-top: 10px; font-size: 0.9em;">
                    <strong>💡 Tip:</strong> Toggle layers using checkboxes above • Legend shows active layers • Click legend items to toggle visibility
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Base map explanation
                base_map_info = ""
                if show_satellite:
                    base_map_info = "🌍 <strong>Satellite View:</strong> Simulated satellite imagery with terrain details"
                elif show_streets:
                    base_map_info = "🗺️ <strong>Street Map View:</strong> Simplified street grid with major highways"
                else:
                    base_map_info = "🏔️ <strong>Physical Map View:</strong> Topographic representation with elevation colors"
                
                st.markdown(f"""
                <div style="background: rgba(100, 150, 255, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0; border-left: 3px solid #6496ff;">
                    <p style="color: #cccccc; margin: 0; font-size: 0.9em;">
                    {base_map_info}<br>
                    • Country borders show political boundaries<br>
                    • Cities marked with population indicators<br>
                    • Grid lines show latitude/longitude coordinates
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Map/Globe controls info
            if st.session_state.map_view == "2d":
                controls_info = """
                <div style="background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #00ff88;">
                    <h4 style="color: #00ff88; margin-top: 0;">🎮 2D Map Controls:</h4>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                        <div>
                            <strong style="color: #ffffff;">🖱️ Navigation:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>Drag:</strong> Pan map<br>
                            • <strong>Scroll:</strong> Zoom in/out<br>
                            • <strong>Click:</strong> Get coordinates
                            </span>
                        </div>
                        <div>
                            <strong style="color: #ffffff;">🗺️ Layers:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • Click <strong>layers icon</strong><br>
                            • Switch between views<br>
                            • Multiple styles available
                            </span>
                        </div>
                        <div>
                            <strong style="color: #ffffff;">🛠️ Tools:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>Measure:</strong> Distance/area<br>
                            • <strong>Fullscreen:</strong> Expand view<br>
                            • <strong>Mini-map:</strong> Overview
                            </span>
                        </div>
                    </div>
                </div>
                """
            else:
                controls_info = """
                <div style="background: rgba(0, 255, 136, 0.1); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #00ff88;">
                    <h4 style="color: #00ff88; margin-top: 0;">🎮 3D Globe Controls:</h4>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                        <div>
                            <strong style="color: #ffffff;">🖱️ Navigation:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>Drag:</strong> Rotate globe<br>
                            • <strong>Scroll:</strong> Zoom in/out<br>
                            • <strong>Right-drag:</strong> Pan view
                            </span>
                        </div>
                        <div>
                            <strong style="color: #ffffff;">🌍 Features:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>3D Earth:</strong> Realistic globe<br>
                            • <strong>Atmosphere:</strong> Glow effect<br>
                            • <strong>Lat/Long:</strong> Grid lines
                            </span>
                        </div>
                        <div>
                            <strong style="color: #ffffff;">🎯 Actions:</strong><br>
                            <span style="color: #cccccc; font-size: 0.9em;">
                            • <strong>Reset:</strong> Default view<br>
                            • <strong>Center:</strong> On study area<br>
                            • <strong>Hover:</strong> See details
                            </span>
                        </div>
                    </div>
                </div>
                """
            
            st.markdown(controls_info, unsafe_allow_html=True)
            
            # Professional GIS information panel
            col1, col2 = st.columns([1, 1])
            with col2:
                current_view_desc = "2D Interactive Map with multiple layers and measurement tools" if st.session_state.map_view == "2d" else "3D Interactive Globe with realistic Earth visualization"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a2a, #2a2a3a); padding: 20px; border-radius: 15px; border: 2px solid #00ff88; box-shadow: 0 8px 25px rgba(0, 255, 136, 0.15);">
                    <h4 style="color: #00ff88; margin-top: 0; text-align: center;">🌍 GIS DATA PANEL</h4>
                    <div style="text-align: center; margin-bottom: 15px;">
                        <span style="background: #00ff88; color: #000000; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">{'2D MAP VIEW' if st.session_state.map_view == '2d' else '3D GLOBE VIEW'}</span>
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
                        <strong style="color: #ffffff;">🔍 Current View:</strong><br>
                        <span style="color: #00ff88;">{current_view_desc}</span>
                    </div>
                    
                    <div style="margin: 15px 0;">
                        <strong style="color: #ffffff;">🔄 Switch View:</strong><br>
                        <span style="color: #cccccc; font-size: 0.9em;">
                        Use sidebar toggle to switch between<br>
                        2D Map and 3D Globe views
                        </span>
                    </div>
                    
                    <div style="background: rgba(0, 255, 136, 0.1); padding: 12px; border-radius: 8px; margin-top: 20px; border-left: 3px solid #00ff88;">
                        <small style="color: #00ff88; display: block; margin-bottom: 5px;">💡 Pro Tip:</small>
                        <small style="color: #888888; font-size: 0.85em;">
                        {'• Switch to 3D Globe for global perspective<br>• Use measurement tools for analysis<br>• Click study area for detailed info' if st.session_state.map_view == '2d' else '• Switch to 2D Map for detailed analysis<br>• Drag to explore different continents<br>• Hover over marker for area details'}
                        </small>
                    </div>
                    
                    <div style="background: #0a0a0a; padding: 10px; border-radius: 5px; margin-top: 20px; text-align: center;">
                        <small style="color: #00ff88;">📊 KHISBA GIS Professional</small><br>
                        <small style="color: #888888;">Hybrid 2D/3D GIS Visualization</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.session_state.selected_geometry = geometry
            
            # Professional status indicator
            view_icon = "🗺️" if st.session_state.map_view == "2d" else "🌐"
            st.markdown(f"""
            <div style="text-align: center; background: linear-gradient(90deg, #00ff88, #004422); padding: 12px; border-radius: 8px; margin: 15px 0; border: 1px solid #ffffff;">
                <strong style="color: white; font-size: 1.1em;">✅ GIS WORKSPACE ACTIVE</strong><br>
                <span style="color: #e8f5e8; font-size: 0.9em;">{view_icon} {area_name} • {area_level} • {view_mode}</span>
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
