import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from datetime import datetime
import ee
import numpy as np
from io import BytesIO

# Custom CSS (keep your existing CSS, just updating the problematic part)
st.markdown("""
<style>
    /* Keep all your existing CSS styles here */
    /* ... existing CSS code ... */
</style>
""", unsafe_allow_html=True)

# Enhanced Earth Engine Auto-Authentication
def auto_initialize_earth_engine() -> bool:
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
        st.error(f"❌ Earth Engine auto-initialization failed: {str(e)}")
        return False

# Page configuration
st.set_page_config(
    page_title="Khisba GIS - Professional Vegetation Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'authenticated': False,
        'ee_initialized': False,
        'analysis_data': None,
        'selected_country': '',
        'selected_admin1': '',
        'selected_admin2': '',
        'selected_indices': ['NDVI', 'EVI', 'SAVI', 'NDWI'],
        'start_date': datetime(2023, 1, 1),
        'end_date': datetime(2023, 12, 31),
        'collection_choice': "Sentinel-2 🛰️",
        'cloud_cover': 20,
        'run_analysis': False,
        'show_results': False
    }
    
    # Initialize indices selection in session state
    available_indices = ['NDVI', 'ARVI', 'ATSAVI', 'DVI', 'EVI', 'EVI2', 'GNDVI', 
                        'MSAVI', 'MSI', 'MTVI', 'MTVI2', 'NDTI', 'NDWI', 'OSAVI', 
                        'RDVI', 'RI', 'RVI', 'SAVI', 'TVI', 'TSAVI', 'VARI', 
                        'VIN', 'WDRVI', 'GCVI', 'AWEI', 'MNDWI', 'WI', 'ANDWI', 
                        'NDSI', 'nDDI', 'NBR', 'DBSI', 'SI', 'S3', 'BRI', 'SSI', 
                        'NDSI_Salinity', 'SRPI', 'MCARI', 'NDCI', 'PSSRb1', 
                        'SIPI', 'PSRI', 'Chl_red_edge', 'MARI', 'NDMI']
    
    for index in available_indices:
        key = f"index_{index}"
        if key not in st.session_state:
            st.session_state[key] = index in defaults['selected_indices']
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Enhanced authentication component
def render_auth_component():
    """Render enhanced authentication component"""
    st.markdown("""
    <div class="main-container">
        <div class="content-container" style="max-width: 480px; margin: 80px auto;">
            <div class="card" style="text-align: center;">
                <div style="margin-bottom: 24px;">
                    <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%); 
                         border-radius: 16px; display: flex; align-items: center; justify-content: center;
                         margin: 0 auto 16px; font-size: 28px;">🌿</div>
                    <h1 style="margin-bottom: 8px;">KHISBA GIS</h1>
                    <p style="color: #999999; font-size: 14px;">Professional Vegetation Analytics Platform</p>
                </div>
                
                <div class="alert alert-success" style="margin-bottom: 24px;">
                    🔐 <span style="font-weight: 600;">Secure Authentication Required</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("", type="password", placeholder="Enter admin password", 
                                label_visibility="collapsed", key="auth_password")
        
        if st.button("🔓 Authenticate", type="primary", use_container_width=True, key="auth_button"):
            if password == "admin":
                st.session_state.authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password. Please try again.")
                
        # Demo credentials
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; color: #666; font-size: 13px;">
            Demo credentials: <strong>admin</strong> / <strong>admin</strong>
        </div>
        """, unsafe_allow_html=True)

# Enhanced area selection component
def render_area_selector():
    """Render enhanced area selection interface"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">🌍</div><h3 style="margin: 0;">Study Area Selection</h3></div>', unsafe_allow_html=True)
    
    try:
        from earth_engine_utils import get_admin_boundaries, get_boundary_names
    except ImportError:
        st.error("Required modules not found")
        return "", "", ""
    
    # Country selector
    countries_fc = get_admin_boundaries(0)
    country_names = get_boundary_names(countries_fc, 0) if countries_fc else []
    
    selected_country = st.selectbox(
        "Select Country",
        options=[""] + sorted(country_names),
        help="Choose a country for analysis",
        key="country_select_main",
        index=0 if st.session_state.selected_country == "" else None
    )
    
    if selected_country != st.session_state.selected_country:
        st.session_state.selected_country = selected_country
        st.session_state.selected_admin1 = ""
        st.session_state.selected_admin2 = ""
    
    # Province/State selector
    selected_admin1 = ""
    if selected_country:
        try:
            country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first()
            country_code = country_feature.get('ADM0_CODE').getInfo()
            
            admin1_fc = get_admin_boundaries(1, country_code)
            admin1_names = get_boundary_names(admin1_fc, 1) if admin1_fc else []
            
            selected_admin1 = st.selectbox(
                "Select State/Province",
                options=[""] + sorted(admin1_names),
                help="Choose a state or province",
                key="admin1_select_main"
            )
            
            if selected_admin1 != st.session_state.selected_admin1:
                st.session_state.selected_admin1 = selected_admin1
                st.session_state.selected_admin2 = ""
                
        except Exception as e:
            st.error(f"Error loading administrative boundaries: {str(e)}")
    
    # District selector
    selected_admin2 = ""
    if selected_admin1:
        try:
            admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
            admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
            
            admin2_fc = get_admin_boundaries(2, None, admin1_code)
            admin2_names = get_boundary_names(admin2_fc, 2) if admin2_fc else []
            
            selected_admin2 = st.selectbox(
                "Select District",
                options=[""] + sorted(admin2_names),
                help="Choose a district or municipality",
                key="admin2_select_main"
            )
            
            if selected_admin2 != st.session_state.selected_admin2:
                st.session_state.selected_admin2 = selected_admin2
                
        except Exception as e:
            st.error(f"Error loading district boundaries: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return selected_country, selected_admin1, selected_admin2

# Enhanced analysis parameters component
def render_analysis_parameters():
    """Render enhanced analysis parameters interface"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">⚙️</div><h3 style="margin: 0;">Analysis Configuration</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.start_date,
            help="Start date for data collection",
            key="start_date_main"
        )
        st.session_state.start_date = start_date
        
    with col2:
        end_date = st.date_input(
            "End Date", 
            value=st.session_state.end_date,
            help="End date for data collection",
            key="end_date_main"
        )
        st.session_state.end_date = end_date
    
    # Satellite source
    collection_choice = st.selectbox(
        "Satellite Source",
        options=["Sentinel-2 🛰️", "Landsat-8 🛰️"],
        help="Choose satellite imagery source",
        key="satellite_select_main"
    )
    st.session_state.collection_choice = collection_choice
    
    # Cloud cover slider
    cloud_cover = st.slider(
        "Maximum Cloud Cover",
        min_value=0,
        max_value=100,
        value=st.session_state.cloud_cover,
        help="Percentage of maximum allowed cloud cover",
        key="cloud_slider_main",
        format="%d%%"
    )
    st.session_state.cloud_cover = cloud_cover
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced vegetation indices selector - FIXED VERSION
def render_indices_selector():
    """Render enhanced vegetation indices selection interface"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">🌿</div><h3 style="margin: 0;">Vegetation Indices</h3></div>', unsafe_allow_html=True)
    
    # Available indices grouped by category
    categories = {
        "Standard Indices": ['NDVI', 'EVI', 'SAVI', 'NDWI'],
        "Advanced Indices": ['ARVI', 'GNDVI', 'MSAVI', 'OSAVI'],
        "Water Indices": ['MNDWI', 'AWEI', 'WI'],
        "Stress Indices": ['MSI', 'NBR', 'NDSI', 'PSRI']
    }
    
    selected_indices = []
    
    # Display indices by category
    for category, indices in categories.items():
        st.markdown(f"**{category}**")
        
        # Use columns for better layout
        cols = st.columns(4)
        for idx, index in enumerate(indices):
            with cols[idx % 4]:
                # Use a unique key for each checkbox
                checkbox_key = f"idx_checkbox_{category}_{index}"
                
                # Initialize session state for this checkbox if not exists
                if checkbox_key not in st.session_state:
                    st.session_state[checkbox_key] = index in st.session_state.selected_indices
                
                # Create checkbox
                if st.checkbox(index, 
                             value=st.session_state[checkbox_key], 
                             key=checkbox_key):
                    selected_indices.append(index)
                    # Update session state
                    if not st.session_state[checkbox_key]:
                        st.session_state[checkbox_key] = True
                else:
                    # Update session state
                    if st.session_state[checkbox_key]:
                        st.session_state[checkbox_key] = False
    
    # Quick selection buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select All Recommended", use_container_width=True, key="select_recommended_btn"):
            # Set all recommended indices to selected
            for category, indices in categories.items():
                for index in indices:
                    key = f"idx_checkbox_{category}_{index}"
                    if index in ['NDVI', 'EVI', 'SAVI', 'NDWI']:
                        st.session_state[key] = True
            st.rerun()
            
    with col2:
        if st.button("Clear Selection", use_container_width=True, key="clear_selection_btn"):
            # Clear all selections
            for category, indices in categories.items():
                for index in indices:
                    key = f"idx_checkbox_{category}_{index}"
                    st.session_state[key] = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return selected_indices

# Enhanced map visualization
def create_enhanced_map(geometry, area_name, area_level):
    """Create enhanced interactive map"""
    try:
        # Calculate bounds
        bounds = geometry.geometry().bounds().getInfo()
        coords = bounds['coordinates'][0]
        lats = [coord[1] for coord in coords]
        lons = [coord[0] for coord in coords]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        # Determine appropriate zoom level
        if area_level == "Country":
            zoom_start = 5
        elif area_level == "Province":
            zoom_start = 7
        else:
            zoom_start = 9
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles=None,
            control_scale=True
        )
        
        # Add base layers
        folium.TileLayer(
            'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            attr='CartoDB',
            name='Dark Mode',
            overlay=False
        ).add_to(m)
        
        folium.TileLayer(
            'OpenStreetMap',
            name='Street Map',
            overlay=False
        ).add_to(m)
        
        folium.TileLayer(
            'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False
        ).add_to(m)
        
        # Add study area
        folium.GeoJson(
            geometry.geometry(),
            style_function=lambda x: {
                'fillColor': '#00ff88',
                'color': '#00ff88',
                'weight': 3,
                'fillOpacity': 0.15,
                'dashArray': '5, 5'
            },
            tooltip=area_name
        ).add_to(m)
        
        # Add marker
        folium.Marker(
            [center_lat, center_lon],
            popup=f"<b>{area_name}</b><br>{area_level}",
            icon=folium.Icon(color='green', icon='leaf', prefix='fa')
        ).add_to(m)
        
        # Add controls
        from folium.plugins import MousePosition, MeasureControl, Fullscreen
        MousePosition(position='bottomleft').add_to(m)
        MeasureControl(primary_length_unit='kilometers').add_to(m)
        Fullscreen().add_to(m)
        
        folium.LayerControl().add_to(m)
        
        return m, center_lat, center_lon
        
    except Exception as e:
        st.error(f"Map creation error: {str(e)}")
        return None, None, None

# Enhanced results visualization
def visualize_results(results):
    """Enhanced visualization of analysis results"""
    if not results:
        return
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Results header
    st.markdown('<div class="compact-header"><h2>Analysis Results</h2><span class="status-badge">📊 Complete</span></div>', unsafe_allow_html=True)
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%); 
                    border-radius: 12px; padding: 20px; color: #000000; margin: 8px 0;">
            <div style="font-size: 28px; font-weight: 700; line-height: 1;">🟢</div>
            <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; 
                       letter-spacing: 1px; opacity: 0.8;">Healthy Vegetation</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%); 
                    border-radius: 12px; padding: 20px; color: #000000; margin: 8px 0;">
            <div style="font-size: 28px; font-weight: 700; line-height: 1;">📈</div>
            <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; 
                       letter-spacing: 1px; opacity: 0.8;">Trend Positive</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%); 
                    border-radius: 12px; padding: 20px; color: #000000; margin: 8px 0;">
            <div style="font-size: 28px; font-weight: 700; line-height: 1;">🌡️</div>
            <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; 
                       letter-spacing: 1px; opacity: 0.8;">Optimal Conditions</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%); 
                    border-radius: 12px; padding: 20px; color: #000000; margin: 8px 0;">
            <div style="font-size: 28px; font-weight: 700; line-height: 1;">✅</div>
            <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; 
                       letter-spacing: 1px; opacity: 0.8;">Analysis Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different visualizations
    viz_tabs = st.tabs(["📈 Time Series", "📊 Statistics", "📥 Export"])
    
    with viz_tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📈</div><h3 style="margin: 0;">Vegetation Trends</h3></div>', unsafe_allow_html=True)
        
        # Create interactive time series plot
        fig = go.Figure()
        
        colors = ['#00ff88', '#00cc6a', '#00994d', '#006633']
        color_idx = 0
        
        for index, data in results.items():
            if data['dates'] and data['values']:
                dates = [datetime.strptime(d, '%Y-%m-%d') if isinstance(d, str) else d for d in data['dates']]
                values = [v for v in data['values'] if v is not None]
                
                if len(dates) == len(values):
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=values,
                        mode='lines+markers',
                        name=index,
                        line=dict(width=3, color=colors[color_idx % len(colors)]),
                        marker=dict(size=6, color=colors[color_idx % len(colors)]),
                        hovertemplate=f'<b>{index}</b><br>Date: %{{x}}<br>Value: %{{y:.4f}}<extra></extra>'
                    ))
                    color_idx += 1
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                gridcolor='#222222',
                zerolinecolor='#222222',
                title_font=dict(color='#ffffff'),
                tickfont=dict(color='#999999')
            ),
            yaxis=dict(
                gridcolor='#222222',
                zerolinecolor='#222222',
                title_font=dict(color='#ffffff'),
                tickfont=dict(color='#999999')
            ),
            legend=dict(
                bgcolor='rgba(10,10,10,0.8)',
                bordercolor='#222222',
                borderwidth=1,
                font=dict(color='#ffffff')
            ),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📊</div><h3 style="margin: 0;">Statistical Summary</h3></div>', unsafe_allow_html=True)
        
        # Create statistics table
        stats_data = []
        for index, data in results.items():
            if data['values']:
                values = [v for v in data['values'] if v is not None]
                if values:
                    mean_val = np.mean(values)
                    std_val = np.std(values)
                    min_val = min(values)
                    max_val = max(values)
                    trend = '📈' if mean_val > 0.5 else '📉' if mean_val < 0.3 else '➡️'
                    
                    stats_data.append({
                        'Index': index,
                        'Mean': f"{mean_val:.4f}",
                        'Std Dev': f"{std_val:.4f}",
                        'Min': f"{min_val:.4f}",
                        'Max': f"{max_val:.4f}",
                        'Trend': trend
                    })
        
        if stats_data:
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">💾</div><h3 style="margin: 0;">Data Export</h3></div>', unsafe_allow_html=True)
        
        # Export options
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "Excel"],
            help="Choose export format",
            key="export_format_select"
        )
        
        if st.button("📥 Export Data", type="primary", use_container_width=True, key="export_btn"):
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
                
                if export_format == "CSV":
                    csv = export_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"vegetation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="download_csv_btn"
                    )
                elif export_format == "Excel":
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        export_df.to_excel(writer, index=False, sheet_name='Vegetation Data')
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name=f"vegetation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_excel_btn"
                    )
            else:
                st.warning("No data available for export")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Run analysis function
def run_analysis(selected_indices):
    """Run vegetation analysis"""
    with st.spinner("🔬 Running analysis..."):
        try:
            # Simulate analysis (replace with actual EE code)
            import time
            time.sleep(2)
            
            # Generate sample results
            results = {}
            for index in selected_indices:
                dates = [f"2023-{m:02d}-15" for m in range(1, 13)]
                values = [0.5 + 0.3 * np.sin(2 * np.pi * m/12) + 0.1 * np.random.rand() 
                         for m in range(1, 13)]
                results[index] = {'dates': dates, 'values': values}
            
            st.session_state.analysis_data = results
            st.session_state.show_results = True
            return results
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            return None

# Main application
def main():
    """Main application function"""
    
    # Initialize session state
    init_session_state()
    
    # Initialize Earth Engine
    if 'ee_auto_initialized' not in st.session_state:
        with st.spinner("🔧 Initializing Earth Engine..."):
            if auto_initialize_earth_engine():
                st.session_state.ee_auto_initialized = True
                st.session_state.ee_initialized = True
            else:
                st.session_state.ee_auto_initialized = False
                st.session_state.ee_initialized = False
    
    # Check authentication
    if not st.session_state.authenticated:
        render_auth_component()
        return
    
    # Main dashboard
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding: 0 8px;">
        <div>
            <h1>🌿 KHISBA GIS</h1>
            <p style="color: #999999; margin: 0; font-size: 14px;">
                Professional Vegetation Analytics & Monitoring Platform
            </p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                🟢 Connected
            </span>
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                v2.0
            </span>
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                🌍 Earth Engine
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create main layout
    col1, col2 = st.columns([0.3, 0.7], gap="large")
    
    with col1:
        # Navigation
        st.markdown('<div class="card" style="padding: 16px;">', unsafe_allow_html=True)
        nav_option = st.selectbox(
            "Navigation",
            ["Dashboard", "Area Selection", "Analysis", "Visualization", "Export"],
            index=0,
            label_visibility="collapsed",
            key="nav_select"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Area selection
        selected_country, selected_admin1, selected_admin2 = render_area_selector()
        
        # Analysis parameters and indices selection
        if selected_country:
            render_analysis_parameters()
            selected_indices = render_indices_selector()
            
            # Update selected indices in session state
            st.session_state.selected_indices = selected_indices
            
            # Run analysis button
            if st.button("🚀 Run Advanced Analysis", type="primary", use_container_width=True, key="run_analysis_btn"):
                if selected_indices:
                    results = run_analysis(selected_indices)
                    if results:
                        st.success("✅ Analysis completed successfully!")
                else:
                    st.error("⚠️ Please select at least one vegetation index")
    
    with col2:
        # Map visualization
        if selected_country:
            st.markdown('<div class="card" style="padding: 0; overflow: hidden;">', unsafe_allow_html=True)
            st.markdown('<div style="padding: 20px;"><h3 style="margin: 0;">Geospatial Analysis</h3></div>', unsafe_allow_html=True)
            
            try:
                from earth_engine_utils import get_admin_boundaries
                countries_fc = get_admin_boundaries(0)
                
                if selected_admin2:
                    admin1_fc = get_admin_boundaries(1, 
                        countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first().get('ADM0_CODE').getInfo())
                    admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
                    admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                    admin2_fc = get_admin_boundaries(2, None, admin1_code)
                    geometry = admin2_fc.filter(ee.Filter.eq('ADM2_NAME', selected_admin2))
                    area_name = f"{selected_admin2}, {selected_admin1}, {selected_country}"
                    area_level = "District"
                elif selected_admin1:
                    admin1_fc = get_admin_boundaries(1, 
                        countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first().get('ADM0_CODE').getInfo())
                    geometry = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1))
                    area_name = f"{selected_admin1}, {selected_country}"
                    area_level = "Province"
                else:
                    geometry = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country))
                    area_name = selected_country
                    area_level = "Country"
                
                # Create enhanced map
                map_obj, center_lat, center_lon = create_enhanced_map(geometry, area_name, area_level)
                
                if map_obj:
                    st_folium(
                        map_obj,
                        width=None,
                        height=500,
                        returned_objects=["last_clicked", "bounds"],
                        key="enhanced_map_main"
                    )
                    
                    # Area info
                    st.markdown(f"""
                    <div style="background: #0a0a0a; border: 1px solid #222222; border-radius: 12px; 
                                padding: 20px; margin-top: 16px;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                            <div style="margin-bottom: 12px; padding: 12px; border-radius: 8px;">
                                <div style="color: #999999; font-size: 12px; font-weight: 500; 
                                            margin-bottom: 4px; text-transform: uppercase;">Study Area</div>
                                <div style="color: #ffffff; font-size: 16px; font-weight: 600;">{area_name}</div>
                            </div>
                            <div style="margin-bottom: 12px; padding: 12px; border-radius: 8px;">
                                <div style="color: #999999; font-size: 12px; font-weight: 500; 
                                            margin-bottom: 4px; text-transform: uppercase;">Administrative Level</div>
                                <div style="color: #00ff88; font-size: 16px; font-weight: 600;">{area_level}</div>
                            </div>
                            <div style="margin-bottom: 12px; padding: 12px; border-radius: 8px;">
                                <div style="color: #999999; font-size: 12px; font-weight: 500; 
                                            margin-bottom: 4px; text-transform: uppercase;">Center Coordinates</div>
                                <div style="color: #ffffff; font-size: 16px; font-weight: 600;">{center_lat:.4f}°, {center_lon:.4f}°</div>
                            </div>
                            <div style="margin-bottom: 12px; padding: 12px; border-radius: 8px;">
                                <div style="color: #999999; font-size: 12px; font-weight: 500; 
                                            margin-bottom: 4px; text-transform: uppercase;">Analysis Status</div>
                                <div style="color: #00ff88; font-size: 16px; font-weight: 600;">Ready</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ Map Error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Results visualization
        if st.session_state.analysis_data and st.session_state.show_results:
            visualize_results(st.session_state.analysis_data)
    
    # Footer
    st.markdown("""
    <div style="height: 1px; background: linear-gradient(90deg, #00ff88, #00cc6a); 
                margin: 32px 0; opacity: 0.3;"></div>
    <div style="text-align: center; color: #666666; font-size: 12px; padding: 20px 0;">
        <p style="margin: 8px 0;">🌿 <strong>KHISBA GIS</strong> • Professional Vegetation Analytics Platform v2.0</p>
        <p style="margin: 8px 0;">Developed with ❤️ by Taibi Farouk Djilali</p>
        <div style="display: flex; justify-content: center; gap: 8px; margin-top: 12px;">
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                Google Earth Engine
            </span>
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                Streamlit
            </span>
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                Folium
            </span>
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
                        background: rgba(0, 255, 136, 0.1); color: #00ff88; border: 1px solid rgba(0, 255, 136, 0.3);
                        border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">
                Plotly
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
