import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from datetime import datetime
import ee
import os

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
if 'selected_geometry' not in st.session_state:
    st.session_state.selected_geometry = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Function to initialize Earth Engine with service account
def initialize_earth_engine():
    """Initialize Earth Engine using the provided service account credentials"""
    try:
        # Your service account credentials (from Streamlit secrets or hardcoded)
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
kcR2Sv7XNX8PL4y2f2XKyPDyiTHb2+dkfyASZtIZh6KeFfyJMFW1BlxAoGAAeG6
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
        st.error(f"Earth Engine initialization failed: {str(e)}")
        return False

# Try to initialize Earth Engine automatically
if not st.session_state.ee_initialized:
    with st.spinner("Initializing Earth Engine..."):
        if initialize_earth_engine():
            st.session_state.ee_initialized = True
            st.session_state.authenticated = True
        else:
            st.error("Failed to initialize Earth Engine")

# Display main interface only if authenticated
if st.session_state.authenticated:
    # Main application header
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(90deg, #1f4037, #99f2c8); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 KHISBA GIS</h1>
    <h3 style="color: #e8f5e8; margin: 10px 0 0 0; font-weight: 300;">Professional Vegetation Indices Analytics</h3>
    <p style="color: #ffffff; font-size: 1.1rem; margin: 15px 0 0 0;">Created by <strong>Taibi Farouk Djilali</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar with status
    st.sidebar.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, #00ff88, #004422); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">📊 KHISBA</h2>
        <p style="color: #e8f5e8; margin: 5px 0 0 0; font-size: 0.9rem;">Professional GIS Trading</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🔐 **AUTHENTICATION STATUS**")
    st.sidebar.success("✅ Earth Engine Connected")
    st.sidebar.markdown(f"""
    <div style="background: #0a0a0a; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <small style="color: #00ff88;">🌐 Online Mode</small><br>
        <small style="color: #888888;">Satellite data: <strong>Available</strong></small>
    </div>
    """, unsafe_allow_html=True)

    # Simplified helper functions (you can add more from your original code)
    def get_admin_boundaries(level, country_code=None, admin1_code=None):
        """Get administrative boundaries"""
        try:
            datasets = {
                0: 'FAO/GAUL/2015/level0',
                1: 'FAO/GAUL/2015/level1',
                2: 'FAO/GAUL/2015/level2'
            }
            
            if level not in datasets:
                return None
                
            fc = ee.FeatureCollection(datasets[level])
            
            if level == 1 and country_code:
                fc = fc.filter(ee.Filter.eq('ADM0_CODE', country_code))
            elif level == 2:
                if admin1_code:
                    fc = fc.filter(ee.Filter.eq('ADM1_CODE', admin1_code))
                elif country_code:
                    fc = fc.filter(ee.Filter.eq('ADM0_CODE', country_code))
                    
            return fc
            
        except Exception as e:
            st.error(f"Error getting boundaries: {e}")
            return None

    def get_boundary_names(fc, level):
        """Extract names from feature collection"""
        try:
            name_columns = {0: 'ADM0_NAME', 1: 'ADM1_NAME', 2: 'ADM2_NAME'}
            name_column = name_columns.get(level, 'ADM0_NAME')
            
            names_list = fc.aggregate_array(name_column).distinct().sort().getInfo()
            return names_list if names_list else []
            
        except Exception as e:
            st.error(f"Error getting names: {e}")
            return []

    # Main application content
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1a1a1a, #2a2a2a); padding: 15px; border-radius: 10px; border-left: 4px solid #00ff88; margin: 20px 0;">
        <h3 style="color: #00ff88; margin: 0;">📍 STUDY AREA SELECTION</h3>
        <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 0.9rem;">Select your geographical area for vegetation analysis</p>
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
                selected_country = ""
        except Exception as e:
            st.error(f"Error loading countries: {str(e)}")
            selected_country = ""
    
    # Simplified analysis section (add your full analysis logic here)
    if selected_country:
        st.success(f"✅ Selected: {selected_country}")
        
        # Get country geometry
        geometry = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country))
        
        # Display map
        try:
            bounds = geometry.geometry().bounds().getInfo()
            coords = bounds['coordinates'][0]
            lats = [coord[1] for coord in coords]
            lons = [coord[0] for coord in coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
            
            m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
            folium.GeoJson(
                bounds,
                style_function=lambda x: {
                    'fillColor': '#00ff88',
                    'color': '#ffffff',
                    'weight': 3,
                    'fillOpacity': 0.2
                }
            ).add_to(m)
            
            st_folium(m, width=800, height=500)
            
            st.session_state.selected_geometry = geometry
            
        except Exception as e:
            st.error(f"Map error: {str(e)}")
    
    # Analysis parameters
    if st.session_state.selected_geometry:
        st.markdown("### ⚙️ Analysis Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
        with col2:
            end_date = st.date_input("End Date", value=datetime(2023, 12, 31))
        
        # Simplified vegetation indices
        available_indices = ['NDVI', 'EVI', 'SAVI', 'NDWI']
        selected_indices = st.multiselect(
            "Vegetation Indices",
            options=available_indices,
            default=['NDVI']
        )
        
        if st.button("🚀 Run Analysis", type="primary"):
            with st.spinner("Analyzing..."):
                try:
                    # Example analysis - you can add your full analysis logic here
                    collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                    filtered = collection.filterDate(
                        start_date.strftime('%Y-%m-%d'), 
                        end_date.strftime('%Y-%m-%d')
                    ).filterBounds(st.session_state.selected_geometry)
                    
                    st.success(f"✅ Found {filtered.size().getInfo()} satellite images")
                    
                    # Create dummy results for demo
                    import random
                    results = {}
                    for index in selected_indices:
                        dates = [f"2023-{m:02d}-15" for m in range(1, 13)]
                        values = [random.uniform(0.1, 0.9) for _ in range(12)]
                        results[index] = {'dates': dates, 'values': values}
                    
                    st.session_state.analysis_results = results
                    
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

    # Display results if available
    if st.session_state.analysis_results:
        st.markdown("### 📊 Results")
        
        for index, data in st.session_state.analysis_results.items():
            st.write(f"**{index}**")
            df = pd.DataFrame({'Date': data['dates'], 'Value': data['values']})
            st.line_chart(df.set_index('Date'))

else:
    # Show loading/error message
    st.error("Application failed to initialize. Please check your credentials.")

# Add your vegetation_indices.py functions here or import them
# For now, I'll create a simple placeholder
def mask_clouds(image):
    return image

def add_vegetation_indices(image):
    return image
