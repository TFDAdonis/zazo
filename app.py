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
from typing import Dict, List, Optional, Tuple
import base64
from io import BytesIO

# Custom CSS for Clean Green & Black TypeScript/React Style
st.markdown("""
<style>
    /* Base styling with dark theme */
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
        --hover-green: rgba(0, 255, 136, 0.1);
        --active-green: rgba(0, 255, 136, 0.2);
        --gradient-green: linear-gradient(135deg, var(--primary-green) 0%, var(--accent-green) 100%);
    }
    
    .stApp {
        background: var(--primary-black);
        color: var(--text-white);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: -0.025em;
        margin: 0;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: var(--gradient-green);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    
    h2 {
        font-size: 1.75rem !important;
        color: var(--primary-green) !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.25rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Layout Container */
    .main-container {
        display: flex;
        gap: 24px;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .sidebar-container {
        width: 320px;
        flex-shrink: 0;
    }
    
    .content-container {
        flex: 1;
        min-width: 0;
    }
    
    /* Cards with glass morphism effect */
    .card {
        background: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-gray);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--gradient-green);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .card:hover {
        border-color: var(--primary-green);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 255, 136, 0.1);
    }
    
    .card:hover::before {
        opacity: 1;
    }
    
    .card-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-gray);
    }
    
    .card-title .icon {
        width: 36px;
        height: 36px;
        background: rgba(0, 255, 136, 0.1);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary-green);
        font-size: 18px;
        transition: all 0.3s ease;
    }
    
    .card:hover .card-title .icon {
        background: rgba(0, 255, 136, 0.2);
        transform: scale(1.05);
    }
    
    /* Buttons with modern design */
    .stButton > button {
        width: 100%;
        background: var(--gradient-green);
        color: var(--primary-black) !important;
        border: none;
        padding: 14px 24px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 8px 0;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.3);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Secondary button */
    div[data-testid="stButton"] button[kind="secondary"] {
        background: transparent !important;
        color: var(--primary-green) !important;
        border: 2px solid var(--primary-green) !important;
    }
    
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: rgba(0, 255, 136, 0.1) !important;
        transform: translateY(-2px);
    }
    
    /* Input fields with modern design */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--secondary-black) !important;
        border: 2px solid var(--border-gray) !important;
        color: var(--text-white) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.1) !important;
        outline: none;
    }
    
    /* Enhanced Select boxes */
    .stSelectbox > div > div {
        background: var(--secondary-black) !important;
        border: 2px solid var(--border-gray) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-green) !important;
    }
    
    /* Enhanced Multi-select */
    .stMultiSelect > div > div > div {
        background: var(--secondary-black) !important;
        border: 2px solid var(--border-gray) !important;
        border-radius: 8px !important;
        min-height: 48px;
    }
    
    .stMultiSelect > div > div > div:hover {
        border-color: var(--primary-green) !important;
    }
    
    /* Modern Sliders */
    .stSlider > div > div > div {
        background: var(--gradient-green) !important;
        height: 6px !important;
        border-radius: 3px !important;
    }
    
    .stSlider > div > div > div > div {
        background: var(--primary-green) !important;
        border: 3px solid var(--primary-black) !important;
        box-shadow: 0 2px 8px rgba(0, 255, 136, 0.4);
        transition: transform 0.2s ease;
    }
    
    .stSlider > div > div > div > div:hover {
        transform: scale(1.2);
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--card-black);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid var(--border-gray);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        background: transparent;
        color: var(--text-gray);
        font-weight: 500;
        transition: all 0.3s ease;
        font-size: 14px;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 136, 0.05);
        color: var(--text-white);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-green) !important;
        color: var(--primary-black) !important;
        border-color: var(--primary-green) !important;
    }
    
    /* Enhanced Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        background: rgba(0, 255, 136, 0.1);
        color: var(--primary-green);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .status-badge:hover {
        background: rgba(0, 255, 136, 0.2);
        transform: translateY(-1px);
    }
    
    /* Modern Alert boxes */
    .alert {
        padding: 16px 20px;
        border-radius: 12px;
        margin: 12px 0;
        border: 2px solid;
        background: var(--card-black);
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease;
    }
    
    .alert:hover {
        transform: translateX(4px);
    }
    
    .alert-success {
        border-color: rgba(0, 255, 136, 0.3);
        color: var(--primary-green);
        background: rgba(0, 255, 136, 0.05);
    }
    
    /* Modern Dataframes */
    .dataframe {
        background: var(--card-black) !important;
        border: 1px solid var(--border-gray) !important;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: var(--secondary-black) !important;
        color: var(--primary-green) !important;
        font-weight: 600 !important;
        border-color: var(--border-gray) !important;
        padding: 16px !important;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
    }
    
    .dataframe td {
        color: var(--text-light-gray) !important;
        border-color: var(--border-gray) !important;
        padding: 14px 16px !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(0, 255, 136, 0.05) !important;
        color: var(--text-white) !important;
    }
    
    /* Modern Tooltips */
    [data-testid="stTooltipIcon"] {
        color: var(--primary-green) !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--secondary-black);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-green);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-green);
    }
    
    /* Section divider */
    .section-divider {
        height: 1px;
        background: var(--gradient-green);
        margin: 32px 0;
        opacity: 0.3;
    }
    
    /* Compact header */
    .compact-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        padding: 0 8px;
    }
    
    /* Modern Info panel */
    .info-panel {
        background: var(--card-black);
        border: 1px solid var(--border-gray);
        border-radius: 12px;
        padding: 20px;
        margin-top: 16px;
    }
    
    .info-item {
        margin-bottom: 12px;
        padding: 12px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .info-item:hover {
        background: rgba(0, 255, 136, 0.05);
    }
    
    .info-label {
        color: var(--text-gray);
        font-size: 12px;
        font-weight: 500;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        color: var(--text-white);
        font-size: 16px;
        font-weight: 600;
    }
    
    /* Analysis status */
    .analysis-status {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 20px;
        background: rgba(0, 255, 136, 0.05);
        border: 2px solid rgba(0, 255, 136, 0.2);
        border-radius: 12px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .analysis-status:hover {
        border-color: var(--primary-green);
        transform: translateX(4px);
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom metrics display */
    .metric-card {
        background: var(--gradient-green);
        border-radius: 12px;
        padding: 20px;
        color: var(--primary-black);
        margin: 8px 0;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.8;
    }
    
    /* Modern form elements */
    .form-row {
        margin-bottom: 20px;
    }
    
    .form-label {
        color: var(--text-gray);
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Map container */
    .map-container {
        border: 2px solid var(--border-gray);
        border-radius: 16px;
        overflow: hidden;
        height: 600px;
        position: relative;
    }
    
    .map-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        box-shadow: inset 0 0 100px rgba(0, 0, 0, 0.3);
        border-radius: 16px;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Custom JavaScript for interactive effects
st.markdown("""
<script>
// Add interactive hover effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = '0 12px 40px rgba(0, 255, 136, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Add loading state to buttons
    const buttons = document.querySelectorAll('.stButton > button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading">⌛</span> Processing...';
            this.disabled = true;
            
            // Reset after 3 seconds (for demo)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });
    
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.card, .section-divider').forEach(el => {
        observer.observe(el);
    });
});
</script>
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
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'ee_initialized' not in st.session_state:
    st.session_state.ee_initialized = False
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'selected_area' not in st.session_state:
    st.session_state.selected_area = None
if 'map_state' not in st.session_state:
    st.session_state.map_state = {
        'center': [0, 0],
        'zoom': 2,
        'bounds': None
    }
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'dashboard'

# Enhanced authentication component
def render_auth_component():
    """Render enhanced authentication component"""
    st.markdown("""
    <div class="main-container">
        <div class="content-container" style="max-width: 480px; margin: 80px auto;">
            <div class="card" style="text-align: center;">
                <div style="margin-bottom: 24px;">
                    <div style="width: 64px; height: 64px; background: var(--gradient-green); 
                         border-radius: 16px; display: flex; align-items: center; justify-content: center;
                         margin: 0 auto 16px; font-size: 28px;">🌿</div>
                    <h1 style="margin-bottom: 8px;">KHISBA GIS</h1>
                    <p style="color: var(--text-gray); font-size: 14px;">Professional Vegetation Analytics Platform</p>
                </div>
                
                <div class="alert alert-success" style="margin-bottom: 24px;">
                    🔐 <span style="font-weight: 600;">Secure Authentication Required</span>
                </div>
                
                <div class="form-row">
                    <div class="form-label">🔑 Enter Admin Password</div>
                </div>
            </div>
            
            <div class="card" style="margin-top: 16px; text-align: center;">
                <p style="color: var(--primary-green); font-weight: 600; margin-bottom: 8px;">Demo Access</p>
                <p style="color: var(--text-gray); font-size: 13px;">Use credentials below for demonstration</p>
                <div style="display: flex; justify-content: center; gap: 8px; margin-top: 12px;">
                    <span class="status-badge">Username: admin</span>
                    <span class="status-badge">Password: admin</span>
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

# Enhanced navigation component
def render_navigation():
    """Render enhanced navigation tabs"""
    tabs = st.tabs(["📊 Dashboard", "🗺️ Map Analysis", "📈 Analytics", "⚙️ Settings"])
    return tabs

# Enhanced area selection component
def render_area_selector():
    """Render enhanced area selection interface"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">🌍</div><h3 style="margin: 0;">Study Area Selection</h3></div>', unsafe_allow_html=True)
    
    try:
        from earth_engine_utils import get_admin_boundaries, get_boundary_names
    except ImportError:
        st.error("Required modules not found")
        return None, None, None
    
    # Country selector with search
    countries_fc = get_admin_boundaries(0)
    country_names = get_boundary_names(countries_fc, 0) if countries_fc else []
    
    selected_country = st.selectbox(
        "Select Country",
        options=[""] + sorted(country_names),
        help="Choose a country for analysis",
        key="country_select",
        index=0
    )
    
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
                key="admin1_select"
            )
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
                key="admin2_select"
            )
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
            value=datetime(2023, 1, 1),
            help="Start date for data collection",
            key="start_date"
        )
    with col2:
        end_date = st.date_input(
            "End Date", 
            value=datetime(2023, 12, 31),
            help="End date for data collection",
            key="end_date"
        )
    
    # Satellite source with icons
    collection_choice = st.selectbox(
        "Satellite Source",
        options=["Sentinel-2 🛰️", "Landsat-8 🛰️"],
        help="Choose satellite imagery source",
        key="satellite_select"
    )
    
    # Cloud cover slider with visual indicator
    cloud_cover = st.slider(
        "Maximum Cloud Cover",
        min_value=0,
        max_value=100,
        value=20,
        help="Percentage of maximum allowed cloud cover",
        key="cloud_slider",
        format="%d%%"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    return start_date, end_date, collection_choice, cloud_cover

# Enhanced vegetation indices selector
def render_indices_selector():
    """Render enhanced vegetation indices selection interface"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title"><div class="icon">🌿</div><h3 style="margin: 0;">Vegetation Indices</h3></div>', unsafe_allow_html=True)
    
    # Categorized indices
    categories = {
        "Standard Indices": ['NDVI', 'EVI', 'SAVI', 'NDWI'],
        "Advanced Indices": ['ARVI', 'GNDVI', 'MSAVI', 'OSAVI'],
        "Water Indices": ['NDWI', 'MNDWI', 'AWEI'],
        "Stress Indices": ['MSI', 'NBR', 'NDSI']
    }
    
    selected_indices = []
    
    for category, indices in categories.items():
        st.markdown(f"**{category}**")
        cols = st.columns(4)
        for idx, index in enumerate(indices):
            with cols[idx % 4]:
                if st.checkbox(index, key=f"index_{index}"):
                    selected_indices.append(index)
    
    # Quick selection buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select All Recommended", use_container_width=True, key="select_recommended"):
            st.session_state.recommended_selected = True
            st.rerun()
    with col2:
        if st.button("Clear Selection", use_container_width=True, key="clear_selection"):
            st.session_state.recommended_selected = False
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
        
        # Create enhanced map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8 if area_level == "Country" else 10 if area_level == "State/Province" else 12,
            tiles=None,
            control_scale=True,
            prefer_canvas=True,
            zoom_control=True,
            scrollWheelZoom=True,
            dragging=True,
            max_bounds=True
        )
        
        # Add base layers
        folium.TileLayer(
            'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
            attr='CartoDB',
            name='Dark Mode',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.TileLayer(
            'OpenStreetMap',
            name='Street Map',
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
        
        # Add study area with enhanced styling
        folium.GeoJson(
            geometry.geometry(),
            style_function=lambda x: {
                'fillColor': '#00ff88',
                'color': '#00ff88',
                'weight': 3,
                'fillOpacity': 0.15,
                'dashArray': '5, 5'
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['ADM2_NAME', 'ADM1_NAME', 'ADM0_NAME'],
                aliases=['District:', 'Province:', 'Country:'],
                localize=True,
                sticky=False,
                labels=True,
                style="""
                    background-color: #0a0a0a;
                    color: #ffffff;
                    border: 2px solid #00ff88;
                    border-radius: 8px;
                    padding: 8px;
                    font-family: 'Inter', sans-serif;
                """
            )
        ).add_to(m)
        
        # Add markers
        folium.Marker(
            [center_lat, center_lon],
            popup=f"<b>{area_name}</b><br>{area_level}",
            icon=folium.Icon(color='green', icon='leaf', prefix='fa')
        ).add_to(m)
        
        # Add plugins
        from folium.plugins import MousePosition, MeasureControl, Fullscreen
        MousePosition(position='bottomleft').add_to(m)
        MeasureControl(primary_length_unit='kilometers').add_to(m)
        Fullscreen().add_to(m)
        
        # Add custom control panel
        from folium import CustomPane
        control_pane = CustomPane(
            html='<div style="background: rgba(10,10,10,0.9); padding: 10px; border-radius: 8px; color: white;">Study Area Active</div>',
            position='topright'
        )
        control_pane.add_to(m)
        
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
        <div class="metric-card">
            <div class="metric-value">🟢</div>
            <div class="metric-label">Healthy Vegetation</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📈</div>
            <div class="metric-label">Trend Positive</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🌡️</div>
            <div class="metric-label">Optimal Conditions</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">✅</div>
            <div class="metric-label">Analysis Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different visualizations
    viz_tabs = st.tabs(["📈 Time Series", "📊 Statistics", "🗺️ Spatial Analysis", "📥 Export"])
    
    with viz_tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">📈</div><h3 style="margin: 0;">Vegetation Trends</h3></div>', unsafe_allow_html=True)
        
        # Create interactive time series plot
        fig = go.Figure()
        
        for index, data in results.items():
            if data['dates'] and data['values']:
                dates = [datetime.fromisoformat(d.replace('Z', '+00:00')) for d in data['dates']]
                values = [v for v in data['values'] if v is not None]
                
                if len(dates) == len(values):
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=values,
                        mode='lines+markers',
                        name=index,
                        line=dict(width=3),
                        marker=dict(size=6),
                        hovertemplate=f'<b>{index}</b><br>Date: %{{x}}<br>Value: %{{y:.4f}}<extra></extra>'
                    ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                gridcolor='var(--border-gray)',
                zerolinecolor='var(--border-gray)',
                title_font=dict(color='var(--text-white)'),
                tickfont=dict(color='var(--text-gray)')
            ),
            yaxis=dict(
                gridcolor='var(--border-gray)',
                zerolinecolor='var(--border-gray)',
                title_font=dict(color='var(--text-white)'),
                tickfont=dict(color='var(--text-gray)')
            ),
            legend=dict(
                bgcolor='rgba(10,10,10,0.8)',
                bordercolor='var(--border-gray)',
                borderwidth=1,
                font=dict(color='var(--text-white)')
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
                    stats_data.append({
                        'Index': index,
                        'Mean': f"{np.mean(values):.4f}",
                        'Std Dev': f"{np.std(values):.4f}",
                        'Min': f"{min(values):.4f}",
                        'Max': f"{max(values):.4f}",
                        'Trend': '📈' if np.polyfit(range(len(values)), values, 1)[0] > 0 else '📉'
                    })
        
        if stats_data:
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with viz_tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><div class="icon">💾</div><h3 style="margin: 0;">Data Export</h3></div>', unsafe_allow_html=True)
        
        # Export options
        export_format = st.selectbox(
            "Export Format",
            ["CSV", "Excel", "JSON"],
            help="Choose export format"
        )
        
        if st.button("📥 Export Data", type="primary", use_container_width=True):
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
                        mime="text/csv"
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
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main application
def main():
    """Main application function"""
    
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
    <div class="compact-header">
        <div>
            <h1>🌿 KHISBA GIS</h1>
            <p style="color: var(--text-gray); margin: 0; font-size: 14px;">
                Professional Vegetation Analytics & Monitoring Platform
            </p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span class="status-badge">🟢 Connected</span>
            <span class="status-badge">v2.0</span>
            <span class="status-badge">🌍 Earth Engine</span>
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
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Area selection
        selected_country, selected_admin1, selected_admin2 = render_area_selector()
        
        # Analysis parameters
        if selected_country:
            start_date, end_date, collection_choice, cloud_cover = render_analysis_parameters()
            selected_indices = render_indices_selector()
            
            # Run analysis button
            if st.button("🚀 Run Advanced Analysis", type="primary", use_container_width=True):
                if selected_indices:
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
                            st.success("✅ Analysis completed successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Analysis failed: {str(e)}")
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
                    geometry = admin2_fc.filter(ee.Filter.eq('ADM2_NAME', selected_admin2))
                    area_name = f"{selected_admin2}, {selected_admin1}, {selected_country}"
                    area_level = "District"
                elif selected_admin1:
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
                        key="enhanced_map"
                    )
                    
                    # Area info
                    st.markdown(f"""
                    <div class="info-panel">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                            <div class="info-item">
                                <div class="info-label">Study Area</div>
                                <div class="info-value">{area_name}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Administrative Level</div>
                                <div class="info-value" style="color: var(--primary-green);">{area_level}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Center Coordinates</div>
                                <div class="info-value">{center_lat:.4f}°, {center_lon:.4f}°</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Analysis Status</div>
                                <div class="info-value" style="color: var(--primary-green);">Ready</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ Map Error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Results visualization
        if st.session_state.analysis_data:
            visualize_results(st.session_state.analysis_data)
    
    # Footer
    st.markdown("""
    <div class="section-divider"></div>
    <div style="text-align: center; color: var(--text-gray); font-size: 12px; padding: 20px 0;">
        <p style="margin: 8px 0;">🌿 <strong>KHISBA GIS</strong> • Professional Vegetation Analytics Platform v2.0</p>
        <p style="margin: 8px 0;">Developed with ❤️ by Taibi Farouk Djilali</p>
        <div style="display: flex; justify-content: center; gap: 8px; margin-top: 12px;">
            <span class="status-badge">Google Earth Engine</span>
            <span class="status-badge">Streamlit</span>
            <span class="status-badge">Folium</span>
            <span class="status-badge">Plotly</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
