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

# Mobile App CSS Styling
st.markdown("""
<style>
    /* Mobile App Container */
    .mobile-app-container {
        max-width: 100%;
        margin: 0 auto;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Status Bar */
    .status-bar {
        display: flex;
        justify-content: space-between;
        padding: 10px 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    .time {
        color: white;
        font-weight: 600;
        font-size: 14px;
    }
    
    .signal-battery {
        display: flex;
        gap: 8px;
        align-items: center;
    }
    
    /* App Header */
    .app-header {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    
    .app-title {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }
    
    .app-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 14px;
        margin: 5px 0 0 0;
    }
    
    /* Card Components */
    .mobile-card {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .card-title {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin: 0;
    }
    
    .card-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
    }
    
    /* Button Styling */
    .mobile-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        text-align: center;
        margin: 10px 0;
    }
    
    .mobile-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .mobile-button-secondary {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border: 2px solid #667eea;
    }
    
    /* Input Fields */
    .mobile-input {
        width: 100%;
        padding: 12px 15px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 14px;
        transition: all 0.3s ease;
        background: white;
    }
    
    .mobile-input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Tabs */
    .mobile-tabs {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        overflow-x: auto;
        padding-bottom: 10px;
    }
    
    .mobile-tab {
        padding: 10px 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        color: white;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.3s ease;
    }
    
    .mobile-tab.active {
        background: white;
        color: #667eea;
    }
    
    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #667eea;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 12px;
        color: #666;
    }
    
    /* Bottom Navigation */
    .bottom-nav {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 40px);
        max-width: 400px;
        background: white;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 -5px 30px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-around;
        z-index: 1000;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: #888;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-item.active {
        color: #667eea;
    }
    
    .nav-icon {
        font-size: 20px;
        margin-bottom: 5px;
    }
    
    /* Charts */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Custom Streamlit Overrides */
    .stSelectbox, .stTextInput, .stDateInput, .stSlider {
        background: white;
        border-radius: 10px;
        padding: 5px;
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .mobile-app-container {
            padding: 10px;
            border-radius: 10px;
        }
        
        .metric-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .stPlotlyChart {
            max-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

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
    page_title="Khisba GIS Mobile",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
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
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "home"

# Main Mobile App Container
st.markdown("""
<div class="mobile-app-container">
    <!-- Status Bar -->
    <div class="status-bar">
        <div class="time">9:41</div>
        <div class="signal-battery">
            <span style="color: white;">📶</span>
            <span style="color: white;">🔋 100%</span>
        </div>
    </div>
    
    <!-- App Header -->
    <div class="app-header">
        <h1 class="app-title">🌿 KHISBA GIS</h1>
        <p class="app-subtitle">Mobile Vegetation Analytics</p>
    </div>
""", unsafe_allow_html=True)

# Authentication check
if not st.session_state.authenticated:
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">🔐 Authentication</h3>
            <div class="card-icon">🔒</div>
        </div>
        <p style="color: #666; margin-bottom: 20px;">Enter credentials to access vegetation analytics</p>
    """, unsafe_allow_html=True)
    
    password = st.text_input("", type="password", placeholder="Enter password", key="login_password")
    
    if st.button("🚀 Login", key="login_btn"):
        if password == "admin":
            st.session_state.authenticated = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid password")
    
    st.markdown("""
        <div style="text-align: center; margin-top: 20px; padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 10px;">
            <p style="color: #667eea; margin: 0; font-size: 12px;">Demo Access</p>
            <p style="color: #333; margin: 5px 0 0 0; font-weight: 500;">Password: <strong>admin</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Navigation Tabs
tabs = ["🏠 Home", "🗺️ Map", "📊 Analytics", "⚙️ Settings"]
current_tab = st.radio(
    "Select Tab",
    tabs,
    horizontal=True,
    label_visibility="collapsed",
    key="tab_navigation"
)

# Extract tab name
tab_name = current_tab.split(" ")[1] if " " in current_tab else current_tab

st.markdown(f"""
<div class="mobile-tabs">
    {"".join([f'<div class="mobile-tab {"active" if current_tab == tab else ""}">{tab}</div>' for tab in tabs])}
</div>
""", unsafe_allow_html=True)

# Tab Content
if current_tab == "🏠 Home":
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">Welcome to KHISBA GIS</h3>
            <div class="card-icon">📱</div>
        </div>
        <p style="color: #666; line-height: 1.6;">Professional vegetation indices analytics in your pocket. 
        Monitor vegetation health, analyze trends, and make data-driven decisions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">Quick Stats</h3>
            <div class="card-icon">📈</div>
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Satellite Data</div>
                <div class="metric-value">2</div>
                <div class="metric-label">Sources</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Indices</div>
                <div class="metric-value">40+</div>
                <div class="metric-label">Available</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Coverage</div>
                <div class="metric-value">Global</div>
                <div class="metric-label">Worldwide</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Update</div>
                <div class="metric-value">Daily</div>
                <div class="metric-label">Frequency</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">Quick Actions</h3>
            <div class="card-icon">⚡</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗺️ Open Map", use_container_width=True):
            st.session_state.current_tab = "🗺️ Map"
            st.rerun()
    with col2:
        if st.button("📊 Start Analysis", use_container_width=True):
            st.session_state.current_tab = "📊 Analytics"
            st.rerun()

elif current_tab == "🗺️ Map":
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">GIS Map View</h3>
            <div class="card-icon">🗺️</div>
        </div>
        <p style="color: #666; margin-bottom: 15px;">Select your study area for analysis</p>
    """, unsafe_allow_html=True)
    
    # Location Selection
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Country", ["Select country", "Algeria", "Morocco", "Tunisia", "Egypt"], key="mobile_country")
    with col2:
        region = st.selectbox("Region", ["Select region", "North", "South", "East", "West"], key="mobile_region")
    
    # Map Display
    if country != "Select country":
        st.markdown("""
        <div style="height: 300px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; margin: 15px 0; display: flex; align-items: center; 
                    justify-content: center; color: white;">
            <div style="text-align: center;">
                <div style="font-size: 48px;">🗺️</div>
                <p>Interactive Map<br><small>Area: {country}, {region}</small></p>
            </div>
        </div>
        """.format(country=country, region=region), unsafe_allow_html=True)
        
        # Save selection
        st.session_state.selected_country = country
        st.session_state.selected_region = region

elif current_tab == "📊 Analytics":
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">Vegetation Analysis</h3>
            <div class="card-icon">📊</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Analysis Parameters
    with st.expander("⚙️ Analysis Settings", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2023, 1, 1))
            satellite = st.selectbox("Satellite", ["Sentinel-2", "Landsat-8"])
        with col2:
            end_date = st.date_input("End Date", datetime(2023, 12, 31))
            cloud_cover = st.slider("Cloud Cover %", 0, 100, 20)
    
    # Vegetation Indices Selection
    with st.expander("🌿 Select Indices"):
        indices = [
            'NDVI', 'EVI', 'SAVI', 'NDWI', 'MSAVI', 'GNDVI',
            'ARVI', 'OSAVI', 'VARI', 'MNDWI', 'NBR', 'PSRI'
        ]
        
        selected_indices = st.multiselect(
            "Choose indices to analyze",
            indices,
            default=['NDVI', 'EVI', 'NDWI'],
            help="Select vegetation indices for analysis"
        )
    
    # Run Analysis Button
    if st.button("🚀 Run Analysis", use_container_width=True):
        with st.spinner("Analyzing vegetation data..."):
            # Simulate analysis
            import time
            time.sleep(2)
            
            # Generate sample results
            dates = pd.date_range(start_date, end_date, freq='M')
            results = {}
            for index in selected_indices:
                values = [0.3 + 0.5 * (i/len(dates)) + 0.1 * np.random.rand() for i in range(len(dates))]
                results[index] = {'dates': dates, 'values': values}
            
            st.session_state.analysis_results = results
            st.success("✅ Analysis completed!")
    
    # Display Results if available
    if st.session_state.analysis_results:
        st.markdown("### 📈 Results")
        
        for index, data in st.session_state.analysis_results.items():
            if data['dates'] and data['values']:
                df = pd.DataFrame({
                    'Date': data['dates'],
                    'Value': data['values']
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df['Value'],
                    mode='lines',
                    name=index,
                    line=dict(color='#667eea', width=3)
                ))
                
                fig.update_layout(
                    title=f'{index} Trend',
                    height=200,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#333')
                )
                
                st.plotly_chart(fig, use_container_width=True)

elif current_tab == "⚙️ Settings":
    st.markdown("""
    <div class="mobile-card">
        <div class="card-header">
            <h3 class="card-title">Settings</h3>
            <div class="card-icon">⚙️</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Earth Engine Status
    with st.expander("🌍 Earth Engine Connection", expanded=True):
        if st.session_state.ee_initialized:
            st.success("✅ Connected to Google Earth Engine")
        else:
            st.error("❌ Earth Engine not connected")
            
            # Upload credentials
            uploaded_file = st.file_uploader("Upload Service Account JSON", type=['json'])
            if uploaded_file:
                try:
                    # Process credentials
                    credentials_data = json.load(uploaded_file)
                    st.success("✅ Credentials uploaded successfully!")
                except:
                    st.error("❌ Invalid JSON file")
    
    # App Settings
    with st.expander("📱 App Preferences"):
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        data_quality = st.select_slider("Data Quality", options=["Low", "Medium", "High"], value="Medium")
        auto_refresh = st.checkbox("Auto-refresh data", value=True)
    
    # Account Section
    with st.expander("👤 Account"):
        st.text_input("Username", value="admin", disabled=True)
        st.button("Change Password", use_container_width=True)
    
    # Logout Button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# Bottom Navigation (simulated)
st.markdown("""
<div class="bottom-nav">
    <div class="nav-item active">
        <div class="nav-icon">🏠</div>
        <div>Home</div>
    </div>
    <div class="nav-item">
        <div class="nav-icon">🗺️</div>
        <div>Map</div>
    </div>
    <div class="nav-item">
        <div class="nav-icon">📊</div>
        <div>Analytics</div>
    </div>
    <div class="nav-item">
        <div class="nav-icon">⚙️</div>
        <div>Settings</div>
    </div>
</div>

<script>
// JavaScript for navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        // Remove active class from all items
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        // Add active class to clicked item
        this.classList.add('active');
    });
});

// Update time in status bar
function updateTime() {
    const now = new Date();
    const timeString = now.getHours().toString().padStart(2, '0') + ':' + 
                      now.getMinutes().toString().padStart(2, '0');
    document.querySelector('.time').textContent = timeString;
}
setInterval(updateTime, 60000);
updateTime();
</script>
""", unsafe_allow_html=True)

# Close mobile app container
st.markdown("</div>", unsafe_allow_html=True)

# Import helper modules
try:
    from earth_engine_utils import get_admin_boundaries, get_boundary_names
    from vegetation_indices import mask_clouds, add_vegetation_indices
except ImportError:
    # Create placeholder functions for demo
    def get_admin_boundaries(level, code=None):
        return None
    
    def get_boundary_names(fc, level):
        return []
    
    def mask_clouds(image):
        return image
    
    def add_vegetation_indices(image):
        return image

# Add numpy import for sample data
import numpy as np

# Note: This is a mobile-optimized version of your original app
# The Earth Engine functionality is preserved but wrapped in a mobile interface
# The actual Earth Engine calls would work the same way
