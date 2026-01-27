import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from datetime import datetime
import ee
import os
from earth_engine_utils import get_admin_boundaries, get_boundary_names
from vegetation_indices import mask_clouds, add_vegetation_indices
import time

# Page configuration
st.set_page_config(
    page_title="Khisba GIS - Vegetation Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Earth Engine ONCE when the app starts
@st.cache_resource
def initialize_earth_engine():
    """Initialize Earth Engine once for the entire app"""
    try:
        # Try to initialize Earth Engine
        ee.Initialize(project='citric-hawk-457513-i6')
        st.session_state.ee_initialized = True
        return True
    except ee.EEException:
        try:
            # If not initialized, try to authenticate and initialize
            ee.Authenticate()
            ee.Initialize(project='citric-hawk-457513-i6')
            st.session_state.ee_initialized = True
            return True
        except:
            # If that fails too, use service account credentials
            try:
                # Try to use environment variable for credentials
                service_account = 'citric-hawk-457513-i6@appspot.gserviceaccount.com'
                credentials = ee.ServiceAccountCredentials(service_account, 'key.json')
                ee.Initialize(credentials, project='citric-hawk-457513-i6')
                st.session_state.ee_initialized = True
                return True
            except:
                st.session_state.ee_initialized = False
                return False

# Initialize Earth Engine at app startup
if 'ee_initialized' not in st.session_state:
    with st.spinner("Initializing Earth Engine..."):
        initialize_earth_engine()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True  # Skip authentication since we're using your EE
if 'selected_geometry' not in st.session_state:
    st.session_state.selected_geometry = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Main application header
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

# Status indicator
st.sidebar.markdown("### 🔐 **SYSTEM STATUS**")

if st.session_state.ee_initialized:
    st.sidebar.success("✅ Earth Engine Connected")
    st.sidebar.markdown(f"""
    <div style="background: #0a0a0a; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <small style="color: #00ff88;">🌐 Online Mode</small><br>
        <small style="color: #888888;">Satellite data: <strong>Available</strong></small>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.error("❌ Earth Engine Error")
    st.sidebar.markdown(f"""
    <div style="background: #2a1a1a; padding: 10px; border-radius: 5px; margin: 10px 0;">
        <small style="color: #ff4444;">⚠️ Connection Failed</small><br>
        <small style="color: #888888;">Please check authentication</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🔄 Retry Connection", type="primary"):
        with st.spinner("Reconnecting to Earth Engine..."):
            if initialize_earth_engine():
                st.sidebar.success("✅ Earth Engine connected!")
                st.rerun()

# Main application logic
if st.session_state.authenticated and st.session_state.ee_initialized:
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
        
        try:
            if selected_country and countries_fc is not None:
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
                
                # Create professional GIS map
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=6,
                    tiles=None,
                    control_scale=True
                )
                
                # Add base layers
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
                
                # Add study area
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
                
                # Add plugins
                from folium.plugins import MousePosition, MeasureControl
                
                MousePosition().add_to(m)
                MeasureControl(primary_length_unit='kilometers').add_to(m)
                folium.LayerControl().add_to(m)
                
                # Display map
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("""
                    <div style="border: 3px solid #00ff88; border-radius: 10px; padding: 5px; background: linear-gradient(45deg, #0a0a0a, #1a1a1a);">
                    """, unsafe_allow_html=True)
                    
                    map_data = st_folium(
                        m, 
                        width=None, 
                        height=500,
                        returned_objects=["last_clicked", "bounds"],
                        key="gis_map"
                    )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    # Information panel
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
                            <strong style="color: #ffffff;">Data Status:</strong><br>
                            <span style="color: #00ff88;">✅ Ready for Analysis</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.selected_geometry = geometry
                
        except Exception as e:
            st.error(f"❌ GIS Map Error: {str(e)}")
            st.info("Please try selecting a different area or check your connection.")
    
    # Professional Analysis Parameters
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
        elif st.session_state.selected_geometry is None:
            st.error("Please select a study area first")
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
                    st.info("This might be due to large area selection or limited data availability. Try selecting a smaller area.")

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
    indices_to_plot = st.multiselect(
        "**Select Vegetation Indices:**",
        options=list(results.keys()),
        default=list(results.keys())[:4] if len(results) >= 4 else list(results.keys()),
        help="Choose vegetation indices to analyze with professional charting"
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
                        
                        # Create professional analytical chart
                        fig = go.Figure()
                        
                        # Main value line
                        current_value = df['Value'].iloc[-1] if len(df) > 0 else 0
                        prev_value = df['Value'].iloc[-2] if len(df) > 1 else current_value
                        is_increasing = current_value >= prev_value
                        
                        fig.add_trace(go.Scatter(
                            x=df['Date'], 
                            y=df['Value'],
                            mode='lines',
                            name=f'{index} Index',
                            line=dict(color='#00ff88' if is_increasing else '#ff4444', width=3),
                            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x}<br>Value: %{y:.4f}<extra></extra>'
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
                                title_font_color='#ffffff'
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
                        
                        # Display chart
                        st.plotly_chart(fig, width='stretch')
                        
                except Exception as e:
                    st.error(f"Error creating chart for {index}: {str(e)}")
    
    # Data Export
    st.subheader("💾 Data Export")
    
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
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"vegetation_indices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data available for export")

elif not st.session_state.ee_initialized:
    st.error("""
    ❌ Earth Engine not initialized!
    
    To fix this issue:
    
    1. **For Local Development:**
       Run this command in your terminal or add it to your main script:
       ```python
       import ee
       ee.Authenticate()  # Run this once to authenticate
       ee.Initialize(project='citric-hawk-457513-i6')
       ```
    
    2. **For Streamlit Cloud Deployment:**
       You need to create a service account key and set it up properly.
    
    3. **Quick Fix for Testing:**
       Modify the initialize_earth_engine() function to use your pre-authenticated credentials.
    """)
    
    if st.button("🔄 Retry Earth Engine Initialization"):
        if initialize_earth_engine():
            st.success("✅ Earth Engine initialized successfully!")
            st.rerun()
        else:
            st.error("Failed to initialize. Please check your credentials.")

elif st.session_state.selected_geometry is None:
    st.info("👆 Please select a study area to proceed with analysis")
else:
    st.info("👆 Configure your analysis parameters and click 'Run Analysis'")
