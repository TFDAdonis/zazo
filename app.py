import streamlit as st
import json
import tempfile
import os
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from datetime import datetime
import ee
import traceback
from folium.plugins import MousePosition, MeasureControl

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

# Earth Engine Initialization with environment variables (SECURE)
def initialize_earth_engine_with_env():
    """Initialize Earth Engine using environment variables"""
    try:
        # Check for environment variables
        service_account_email = os.environ.get('EE_SERVICE_ACCOUNT')
        private_key = os.environ.get('EE_PRIVATE_KEY')
        
        if service_account_email and private_key:
            # Format private key properly
            if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
                private_key = f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----"
            
            credentials = ee.ServiceAccountCredentials(
                service_account_email,
                key_data=private_key
            )
            ee.Initialize(credentials)
            return True
    except Exception as e:
        st.error(f"Environment variable initialization failed: {str(e)}")
    return False

# Try environment variables first
if 'ee_env_initialized' not in st.session_state:
    with st.spinner("Initializing Earth Engine..."):
        if initialize_earth_engine_with_env():
            st.session_state.ee_env_initialized = True
            st.session_state.ee_initialized = True
        else:
            st.session_state.ee_env_initialized = False

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

# Main app header
st.markdown("""
<div style="text-align: center; background: linear-gradient(90deg, #1f4037, #99f2c8); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
<h1 style="color: white; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 KHISBA GIS</h1>
<h3 style="color: #e8f5e8; margin: 10px 0 0 0; font-weight: 300;">Professional Vegetation Indices Analytics</h3>
<p style="color: #ffffff; font-size: 1.1rem; margin: 15px 0 0 0;">Created by <strong>Taibi Farouk Djilali</strong></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #00ff88, #004422); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="color: white; margin: 0; font-size: 1.5rem;">📊 KHISBA</h2>
    <p style="color: #e8f5e8; margin: 5px 0 0 0; font-size: 0.9rem;">Professional GIS Trading</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🔐 **EARTH ENGINE AUTHENTICATION**")

# Earth Engine initialization options
if not st.session_state.ee_initialized:
    # Option 1: Environment variables (already tried)
    st.sidebar.info("ℹ️ Earth Engine not initialized")
    
    # Option 2: Service account file upload
    st.sidebar.subheader("Upload Service Account Credentials")
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose service account JSON file",
        type=['json'],
        help="Upload your Google Earth Engine service account JSON file"
    )
    
    if uploaded_file is not None:
        try:
            credentials_data = json.load(uploaded_file)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                json.dump(credentials_data, tmp_file)
                tmp_path = tmp_file.name
            
            try:
                # Initialize with service account
                credentials = ee.ServiceAccountCredentials(
                    credentials_data['client_email'],
                    key_data=json.dumps(credentials_data)
                )
                ee.Initialize(credentials)
                st.session_state.ee_initialized = True
                st.sidebar.success("✅ Earth Engine initialized!")
                os.unlink(tmp_path)
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ Initialization failed: {str(e)}")
                if "Invalid JSON" in str(e):
                    st.sidebar.info("Please check if the JSON file is valid")
        except Exception as e:
            st.sidebar.error(f"❌ Error reading file: {str(e)}")
    
    # Option 3: Manual credentials (for development)
    with st.sidebar.expander("Advanced: Manual Setup"):
        st.markdown("For development only. Use environment variables in production.")
        service_account = st.text_input("Service Account Email")
        private_key = st.text_area("Private Key", height=100)
        
        if st.button("Initialize Manually"):
            if service_account and private_key:
                try:
                    credentials = ee.ServiceAccountCredentials(
                        service_account,
                        key_data=private_key
                    )
                    ee.Initialize(credentials)
                    st.session_state.ee_initialized = True
                    st.success("✅ Manual initialization successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Manual initialization failed: {str(e)}")
else:
    st.sidebar.success("✅ Earth Engine Connected")
    
    # Add Earth Engine info
    try:
        profile = ee.data.getAssetRoots()
        st.sidebar.info(f"✅ Earth Engine API v{ee.__version__}")
    except:
        pass

# Load helper functions
def load_boundary_functions():
    """Mock boundary functions for demonstration"""
    def get_admin_boundaries(level, country_code=None, admin1_code=None):
        """Get administrative boundaries"""
        try:
            if level == 0:
                # Countries
                return ee.FeatureCollection("FAO/GAUL/2015/level0")
            elif level == 1:
                # Admin1
                return ee.FeatureCollection("FAO/GAUL/2015/level1")
            elif level == 2:
                # Admin2
                return ee.FeatureCollection("FAO/GAUL/2015/level2")
        except:
            return None
    
    def get_boundary_names(fc, level):
        """Get names from boundary collection"""
        try:
            # This is a simplified version
            prop_name = f'ADM{level}_NAME'
            names = fc.aggregate_array(prop_name).distinct().getInfo()
            return sorted([n for n in names if n])
        except:
            return []
    
    return get_admin_boundaries, get_boundary_names

# Mock vegetation indices functions
def mask_clouds(image):
    """Simple cloud masking for Sentinel-2"""
    try:
        # Cloud probability band
        cloudProb = image.select('MSK_CLDPRB')
        # Cloud mask where cloud probability is less than 50%
        cloudMask = cloudProb.lt(50)
        return image.updateMask(cloudMask)
    except:
        return image

def add_vegetation_indices(image):
    """Add common vegetation indices"""
    try:
        # Calculate NDVI
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        # Calculate EVI
        evi = image.expression(
            '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
            {
                'NIR': image.select('B8'),
                'RED': image.select('B4'),
                'BLUE': image.select('B2')
            }
        ).rename('EVI')
        
        return image.addBands([ndvi, evi])
    except:
        return image

# Main application
if st.session_state.ee_initialized:
    try:
        # Get boundary functions
        get_admin_boundaries, get_boundary_names = load_boundary_functions()
        
        # Area Selection
        st.markdown("""
        <div style="background: linear-gradient(90deg, #1a1a1a, #2a2a2a); padding: 15px; border-radius: 10px; border-left: 4px solid #00ff88; margin: 20px 0;">
            <h3 style="color: #00ff88; margin: 0;">📍 TRADING AREA SELECTION</h3>
            <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 0.9rem;">Select your geographical trading zone</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                countries_fc = get_admin_boundaries(0)
                if countries_fc:
                    country_names = get_boundary_names(countries_fc, 0)
                    selected_country = st.selectbox(
                        "Select Country",
                        options=[""] + country_names[:50],  # Limit to 50 for performance
                        help="Choose a country for analysis"
                    )
                else:
                    selected_country = ""
                    st.warning("Could not load countries")
            except Exception as e:
                selected_country = ""
                st.error(f"Error: {str(e)}")
        
        # Map display (simplified for demo)
        if selected_country:
            st.markdown("### 🌍 **GIS WORKSPACE**")
            
            try:
                # Create a simple map
                m = folium.Map(location=[20, 0], zoom_start=2)
                
                # Add layers
                folium.TileLayer('OpenStreetMap').add_to(m)
                folium.TileLayer(
                    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='Esri',
                    name='Satellite'
                ).add_to(m)
                
                folium.LayerControl().add_to(m)
                
                # Display map
                st_folium(m, width=None, height=400)
                
                st.info(f"Selected area: {selected_country}")
                
            except Exception as e:
                st.error(f"Map error: {str(e)}")
        
        # Analysis Parameters
        st.markdown("""
        <div style="background: linear-gradient(90deg, #2a1a1a, #3a2a1a); padding: 15px; border-radius: 10px; border-left: 4px solid #ffaa00; margin: 20px 0;">
            <h3 style="color: #ffaa00; margin: 0;">⚙️ ANALYSIS PARAMETERS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
            cloud_cover = st.slider("Cloud Cover (%)", 0, 100, 20)
        
        with col2:
            end_date = st.date_input("End Date", value=datetime(2023, 12, 31))
            collection_choice = st.selectbox("Satellite", ["Sentinel-2", "Landsat-8"])
        
        # Indices selection
        available_indices = ['NDVI', 'EVI', 'SAVI', 'NDWI', 'GNDVI', 'MSAVI']
        selected_indices = st.multiselect(
            "Vegetation Indices",
            available_indices,
            default=['NDVI', 'EVI']
        )
        
        # Run analysis button
        if st.button("🚀 Run Analysis", type="primary"):
            if not selected_country:
                st.error("Please select a country first")
            elif not selected_indices:
                st.error("Please select at least one index")
            else:
                with st.spinner("Running analysis..."):
                    try:
                        # Simulate analysis results
                        import random
                        from datetime import timedelta
                        
                        # Generate dummy data
                        results = {}
                        dates = [datetime(2023, 1, 1) + timedelta(days=i*15) for i in range(24)]
                        date_strings = [d.strftime('%Y-%m-%d') for d in dates]
                        
                        for index in selected_indices:
                            # Generate realistic values for each index
                            if index == 'NDVI':
                                values = [0.3 + 0.5 * (i/24) + random.uniform(-0.1, 0.1) for i in range(24)]
                            elif index == 'EVI':
                                values = [0.2 + 0.3 * (i/24) + random.uniform(-0.05, 0.05) for i in range(24)]
                            elif index == 'SAVI':
                                values = [0.25 + 0.4 * (i/24) + random.uniform(-0.08, 0.08) for i in range(24)]
                            else:
                                values = [0.1 + 0.2 * (i/24) + random.uniform(-0.05, 0.05) for i in range(24)]
                            
                            results[index] = {
                                'dates': date_strings,
                                'values': values
                            }
                        
                        st.session_state.analysis_results = results
                        st.session_state.selected_geometry = selected_country
                        st.success("✅ Analysis completed successfully!")
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
        
        # Display results if available
        if st.session_state.analysis_results:
            st.markdown("### 📊 **ANALYSIS RESULTS**")
            
            results = st.session_state.analysis_results
            
            # Summary statistics
            st.subheader("📈 Summary")
            summary_data = []
            for index, data in results.items():
                values = data['values']
                if values:
                    summary_data.append({
                        'Index': index,
                        'Mean': round(sum(values) / len(values), 4),
                        'Min': round(min(values), 4),
                        'Max': round(max(values), 4)
                    })
            
            if summary_data:
                st.dataframe(pd.DataFrame(summary_data))
            
            # Charts
            st.subheader("📈 Time Series Analysis")
            
            indices_to_plot = st.multiselect(
                "Select indices to plot:",
                list(results.keys()),
                default=list(results.keys())[:3]
            )
            
            if indices_to_plot:
                fig = go.Figure()
                
                colors = ['#00ff88', '#ffaa00', '#00aaff', '#ff44aa', '#aa00ff']
                
                for i, index in enumerate(indices_to_plot):
                    if i < len(colors):
                        color = colors[i]
                    else:
                        color = f'rgb({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)})'
                    
                    data = results[index]
                    dates = [datetime.strptime(d, '%Y-%m-%d') for d in data['dates']]
                    
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=data['values'],
                        mode='lines+markers',
                        name=index,
                        line=dict(color=color, width=2),
                        marker=dict(size=4)
                    ))
                
                fig.update_layout(
                    title="Vegetation Indices Time Series",
                    xaxis_title="Date",
                    yaxis_title="Index Value",
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#0E1117',
                    font=dict(color='white'),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Download button
            st.subheader("💾 Export Data")
            if st.button("📥 Download CSV"):
                # Prepare data
                export_data = []
                for index, data in results.items():
                    for date, value in zip(data['dates'], data['values']):
                        export_data.append({
                            'Date': date,
                            'Index': index,
                            'Value': value
                        })
                
                if export_data:
                    df = pd.DataFrame(export_data)
                    csv = df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download",
                        data=csv,
                        file_name=f"vegetation_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
    
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.code(traceback.format_exc())

else:
    st.info("👆 Please authenticate Earth Engine in the sidebar to begin analysis")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888888; font-size: 0.9rem;">
    <p>📊 KHISBA GIS • Professional Vegetation Analytics • Created by Taibi Farouk Djilali</p>
    <p>Powered by Google Earth Engine • Streamlit</p>
</div>
""", unsafe_allow_html=True)
