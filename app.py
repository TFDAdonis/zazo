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
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 0;
        padding-right: 0;
        max-width: 100%;
    }
    
    /* Main container */
    .main-container {
        display: flex;
        height: 100vh;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Left sidebar */
    .sidebar-left {
        width: 380px;
        background: #111111;
        padding: 24px;
        border-right: 1px solid #222222;
        overflow-y: auto;
        flex-shrink: 0;
    }
    
    /* Main content area */
    .main-content {
        flex: 1;
        padding: 24px;
        overflow-y: auto;
        background: #000000;
    }
    
    /* Title styling */
    .app-title {
        font-size: 24px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 4px;
        background: linear-gradient(90deg, #00ff88, #00cc6a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-subtitle {
        font-size: 14px;
        color: #999999;
        margin-bottom: 32px;
        font-weight: 400;
    }
    
    /* Section styling */
    .section {
        margin-bottom: 32px;
    }
    
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Input groups */
    .input-group {
        margin-bottom: 20px;
    }
    
    .input-label {
        font-size: 14px;
        color: #cccccc;
        margin-bottom: 8px;
        display: block;
        font-weight: 500;
    }
    
    /* Custom input styling */
    .custom-input {
        background: #0a0a0a !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        width: 100%;
    }
    
    .custom-input:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.1) !important;
        outline: none !important;
    }
    
    /* Select box styling */
    .custom-select {
        background: #0a0a0a !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
        width: 100%;
        height: 40px;
    }
    
    /* Checkbox styling */
    .custom-checkbox {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }
    
    .checkbox-label {
        font-size: 14px;
        color: #cccccc;
        font-weight: 500;
    }
    
    /* Button styling */
    .primary-button {
        background: linear-gradient(90deg, #00ff88, #00cc6a) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        width: 100%;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .primary-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.2);
    }
    
    /* Map container */
    .map-container {
        background: #0a0a0a;
        border: 1px solid #333333;
        border-radius: 8px;
        overflow: hidden;
        height: 500px;
        margin-bottom: 24px;
    }
    
    /* Map controls */
    .map-controls {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        font-size: 14px;
        color: #cccccc;
    }
    
    .control-badge {
        background: rgba(0, 255, 136, 0.1);
        color: #00ff88;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: #222222;
        margin: 24px 0;
    }
    
    /* Options section */
    .options-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 16px;
    }
    
    .option-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px;
        background: #0a0a0a;
        border: 1px solid #333333;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .option-item:hover {
        border-color: #00ff88;
        background: rgba(0, 255, 136, 0.05);
    }
    
    .option-label {
        font-size: 14px;
        color: #cccccc;
        font-weight: 500;
    }
    
    /* Status message */
    .status-message {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 6px;
        padding: 12px;
        margin-top: 24px;
        font-size: 13px;
        color: #00ff88;
        text-align: center;
    }
    
    /* Hide Streamlit elements */
    .stButton > button {
        all: unset;
    }
    
    div[data-testid="stTextInput"] > div > div > input,
    div[data-testid="stSelectbox"] > div > div > div,
    div[data-testid="stCheckbox"] > label {
        all: unset;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #333333;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #444444;
    }
</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="KHISBA GIS - Vegetation Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True  # Skip auth for demo
if 'ee_initialized' not in st.session_state:
    st.session_state.ee_initialized = True  # Skip EE init for demo

# Main layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# LEFT SIDEBAR - Controls
st.markdown('<div class="sidebar-left">', unsafe_allow_html=True)

# Title
st.markdown('<div class="app-title">KHISBA GIS</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Vegetation Analytics</div>', unsafe_allow_html=True)

# Quick Setup Section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Quick setup</div>', unsafe_allow_html=True)

# Area Name
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Area name</div>', unsafe_allow_html=True)
area_name = st.text_input(
    "",
    value="KHISBA_Test_AOI_01",
    key="area_name",
    label_visibility="collapsed"
)
st.markdown('<div style="font-size: 12px; color: #666666; margin-top: 4px;">Use Draw/Upload in the map panel (placeholder).</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Vegetation Index Selection
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Vegetation Index</div>', unsafe_allow_html=True)

# Create a custom select box look using columns
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown('<div style="padding: 10px; background: #0a0a0a; border: 1px solid #333333; border-radius: 6px 0 0 6px; border-right: none; height: 40px; display: flex; align-items: center; justify-content: center; color: #00ff88;">NDVI</div>', unsafe_allow_html=True)
with col2:
    selected_index = st.selectbox(
        "",
        options=["NDVI", "EVI", "SAVI", "NDWI", "GNDVI", "MSAVI"],
        index=0,
        label_visibility="collapsed",
        key="index_select"
    )

st.markdown('<div style="font-size: 12px; color: #666666; margin-top: 4px;">Vegetation vigor</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Run Analysis Button
if st.button("🚀 Run analysis", key="run_analysis"):
    st.session_state.analysis_ran = True
    st.rerun()

st.markdown('<div class="status-message">Analysis is simulated for the mockup.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End Quick Setup section

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# More Options Section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚙️ More options</div>', unsafe_allow_html=True)

# Cloud max
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Cloud max</div>', unsafe_allow_html=True)
cloud_max = st.slider(
    "",
    min_value=0,
    max_value=100,
    value=20,
    format="%d%%",
    label_visibility="collapsed",
    key="cloud_slider"
)
st.markdown('</div>', unsafe_allow_html=True)

# Apply mask checkbox
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<div class="custom-checkbox">', unsafe_allow_html=True)
apply_mask = st.checkbox("Apply mask", value=True, key="apply_mask")
st.markdown('<div class="checkbox-label">Apply mask</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size: 12px; color: #666666; margin-top: -8px; margin-bottom: 16px;">Reduce false positives.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End More Options section

# Map Controls Section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🗺️ Options</div>', unsafe_allow_html=True)

# Map control buttons
st.markdown('<div class="options-grid">', unsafe_allow_html=True)

# Basemap
st.markdown("""
<div class="option-item">
    <span style="color: #00ff88;">🗺️</span>
    <span class="option-label">Basemap</span>
</div>
""", unsafe_allow_html=True)

# Layers
st.markdown("""
<div class="option-item">
    <span style="color: #00ff88;">📊</span>
    <span class="option-label">Layers</span>
</div>
""", unsafe_allow_html=True)

# Draw
st.markdown("""
<div class="option-item">
    <span style="color: #00ff88;">✏️</span>
    <span class="option-label">Draw</span>
</div>
""", unsafe_allow_html=True)

# Upload
st.markdown("""
<div class="option-item">
    <span style="color: #00ff88;">📁</span>
    <span class="option-label">Upload</span>
</div>
""", unsafe_allow_html=True)

# Center
st.markdown("""
<div class="option-item">
    <span style="color: #00ff88;">📍</span>
    <span class="option-label">Center</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End options grid

st.markdown('</div>', unsafe_allow_html=True)  # End Options section

st.markdown('</div>', unsafe_allow_html=True)  # End left sidebar

# MAIN CONTENT AREA - Map
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Map title and controls
st.markdown('<div style="margin-bottom: 16px;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🗺️ Map</div>', unsafe_allow_html=True)

# Map controls display
st.markdown('<div class="map-controls">', unsafe_allow_html=True)
st.markdown(f'Draw / Upload area (visual placeholder)', unsafe_allow_html=True)
st.markdown('<div style="flex: 1;"></div>', unsafe_allow_html=True)
st.markdown('<div class="control-badge">NDVI</div>', unsafe_allow_html=True)
st.markdown('<div class="control-badge">cloud ≤ {cloud_max}%</div>'.format(cloud_max=cloud_max), unsafe_allow_html=True)
st.markdown('<div class="control-badge">mask: on</div>', unsafe_allow_html=True)
st.markdown('<div class="control-badge">smooth: on</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Map container
st.markdown('<div class="map-container">', unsafe_allow_html=True)

# Create a simple map placeholder with Folium
try:
    # Create a centered map (Morocco coordinates for demo)
    m = folium.Map(
        location=[31.7917, -7.0926],
        zoom_start=6,
        tiles=None,
        control_scale=True,
        prefer_canvas=True
    )
    
    # Add tile layers
    folium.TileLayer(
        'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='CartoDB',
        name='Dark Map',
        overlay=False,
        control=False
    ).add_to(m)
    
    # Add a sample polygon (rectangle for demo)
    sample_bounds = [[30.5, -8.5], [33.5, -5.5]]
    folium.Rectangle(
        bounds=sample_bounds,
        color='#00ff88',
        weight=2,
        fill=True,
        fill_color='#00ff88',
        fill_opacity=0.1,
        dash_array='5, 5'
    ).add_to(m)
    
    # Add text overlay
    folium.map.Marker(
        [32.0, -7.0],
        icon=folium.DivIcon(
            html='<div style="font-family: Arial; font-size: 14px; color: #00ff88; background: rgba(0,0,0,0.7); padding: 8px; border-radius: 4px; border: 1px solid #00ff88;">KHISBA_Test_AOI_01</div>'
        )
    ).add_to(m)
    
    # Display the map
    st_folium(m, width=None, height=480, returned_objects=[], key="map")
    
except Exception as e:
    # Fallback placeholder if map fails
    st.markdown(f"""
    <div style="height: 480px; background: linear-gradient(135deg, #0a0a0a 0%, #111111 100%); display: flex; align-items: center; justify-content: center; color: #666666; font-size: 14px; border-radius: 8px;">
        <div style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">🗺️</div>
            <div>Interactive Map Display</div>
            <div style="margin-top: 8px; color: #00ff88;">KHISBA_Test_AOI_01</div>
            <div style="margin-top: 16px; color: #999999; font-size: 12px;">Click map controls to draw or upload areas</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End map container

# Analysis Results (if analysis was run)
if st.session_state.get('analysis_ran', False):
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Results header
    st.markdown('<div style="margin-bottom: 24px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Analysis Results</div>', unsafe_allow_html=True)
    
    # Create sample data for visualization
    dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
    ndvi_values = [0.3 + 0.4 * (abs((i - 6) / 12)) + 0.1 * np.random.randn() for i in range(len(dates))]
    
    # Create a Plotly chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=ndvi_values,
        mode='lines+markers',
        name='NDVI',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=6, color='#000000', line=dict(width=2, color='#00ff88'))
    ))
    
    # Add a filled area under the line
    fig.add_trace(go.Scatter(
        x=dates,
        y=[0.2] * len(dates),
        fill='tonexty',
        mode='none',
        fillcolor='rgba(0, 255, 136, 0.1)',
        name='Vegetation Baseline'
    ))
    
    # Update layout
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#000000',
        font=dict(color='#ffffff', size=12),
        xaxis=dict(
            gridcolor='#222222',
            linecolor='#333333',
            tickformat='%b %Y'
        ),
        yaxis=dict(
            gridcolor='#222222',
            linecolor='#333333',
            range=[0, 1]
        ),
        hovermode='x unified',
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='#333333',
            borderwidth=1
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #0a0a0a; border: 1px solid #333333; border-radius: 6px; padding: 16px;">
            <div style="font-size: 12px; color: #999999; margin-bottom: 4px;">Average NDVI</div>
            <div style="font-size: 24px; font-weight: 600; color: #00ff88;">0.52</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #0a0a0a; border: 1px solid #333333; border-radius: 6px; padding: 16px;">
            <div style="font-size: 12px; color: #999999; margin-bottom: 4px;">Peak Value</div>
            <div style="font-size: 24px; font-weight: 600; color: #00ff88;">0.78</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #0a0a0a; border: 1px solid #333333; border-radius: 6px; padding: 16px;">
            <div style="font-size: 12px; color: #999999; margin-bottom: 4px;">Vegetation Health</div>
            <div style="font-size: 24px; font-weight: 600; color: #00ff88;">Good</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #0a0a0a; border: 1px solid #333333; border-radius: 6px; padding: 16px;">
            <div style="font-size: 12px; color: #999999; margin-bottom: 4px;">Area Size</div>
            <div style="font-size: 24px; font-weight: 600; color: #00ff88;">256 km²</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End main content

st.markdown('</div>', unsafe_allow_html=True)  # End main container

# Footer
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background: #0a0a0a; border-top: 1px solid #222222; padding: 12px 24px; font-size: 12px; color: #666666; display: flex; justify-content: space-between; align-items: center;">
    <div>KHISBA GIS • Vegetation Analytics Platform</div>
    <div style="display: flex; gap: 16px;">
        <span style="color: #00ff88;">🌿 Ready</span>
        <span>|</span>
        <span>v1.0</span>
    </div>
</div>
""", unsafe_allow_html=True)
