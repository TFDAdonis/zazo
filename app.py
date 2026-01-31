# Replace the Custom CSS section with this:
st.markdown("""
<style>
    /* Base styling - TypeScript/React style */
    .stApp {
        background: #0f0f0f;
        color: #e0e0e0;
        font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    /* Remove Streamlit default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* KHISBA GIS Header - Exact match to screenshot */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        background: #1a1a1a;
        border-bottom: 1px solid #2a2a2a;
        margin-bottom: 1.5rem;
        border-radius: 8px;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .app-logo {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ff88, #00cc6a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        color: #888;
        font-size: 0.875rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Clean panel styling - like screenshot */
    .clean-panel {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .panel-title {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: -0.25px;
        margin: 0;
    }
    
    .panel-subtitle {
        color: #888;
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    /* Form elements - Clean React style */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #252525 !important;
        border: 1px solid #3a3a3a !important;
        color: #e0e0e0 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-size: 0.875rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.1) !important;
        outline: none !important;
    }
    
    /* Labels */
    .form-label {
        color: #aaa;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Buttons - Clean style */
    .stButton > button {
        background: #00ff88 !important;
        color: #000000 !important;
        border: none !important;
        padding: 10px 16px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.25px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #00cc6a !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.2) !important;
    }
    
    /* Checkboxes - Clean toggle style */
    .stCheckbox > label {
        color: #e0e0e0 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00ff88, #00cc6a) !important;
    }
    
    .stSlider > div > div > div > div {
        background: #ffffff !important;
        border: 2px solid #00ff88 !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #252525 !important;
        border: 1px solid #3a3a3a !important;
    }
    
    /* Multi-select */
    .stMultiSelect > div > div > div {
        background: #252525 !important;
        border: 1px solid #3a3a3a !important;
    }
    
    /* Status badges - like screenshot */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 8px;
        background: rgba(0, 255, 136, 0.1);
        color: #00ff88;
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Map container - Clean frame */
    .map-container {
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        overflow: hidden;
        background: #1a1a1a;
    }
    
    /* Analysis card - like "Quick setup" in screenshot */
    .analysis-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .analysis-header {
        color: #ffffff;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #2a2a2a;
    }
    
    /* Options panel - like "More options" in screenshot */
    .options-panel {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Compact layout */
    .compact-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .compact-item {
        flex: 1;
    }
    
    /* Info displays */
    .info-display {
        background: #252525;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .info-label {
        color: #888;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .info-value {
        color: #ffffff;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    /* Run analysis button - prominent */
    .run-analysis-btn {
        background: linear-gradient(90deg, #00ff88, #00cc6a) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        margin-top: 1rem !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Divider */
    .divider {
        height: 1px;
        background: #2a2a2a;
        margin: 1.5rem 0;
    }
    
    /* Two-column layout */
    .two-col-layout {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 1.5rem;
        align-items: start;
    }
    
    @media (max-width: 1200px) {
        .two-col-layout {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Then update the main layout structure:

# Replace the Main Dashboard Layout section with:
st.markdown("""
<div class="main-header">
    <div class="header-left">
        <div class="app-logo">KHISBA GIS</div>
        <div class="app-subtitle">Vegetation Analytics</div>
    </div>
    <div>
        <span class="status-badge">Earth Engine Ready</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Update the main layout structure:
st.markdown('<div class="two-col-layout">', unsafe_allow_html=True)

# LEFT COLUMN (Controls) - matches screenshot layout
with st.container():
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><h3 class="panel-title">Quick setup</h3></div>', unsafe_allow_html=True)
    
    # Area selection
    st.markdown('<div class="form-label">Area name</div>', unsafe_allow_html=True)
    
    if st.session_state.ee_initialized:
        try:
            countries_fc = get_admin_boundaries(0)
            if countries_fc is not None:
                country_names = get_boundary_names(countries_fc, 0)
                selected_country = st.selectbox(
                    "",
                    options=["Select country"] + country_names,
                    help="Choose a country for analysis",
                    key="country_select",
                    label_visibility="collapsed"
                )
                
                if selected_country and selected_country != "Select country":
                    st.info(f"Selected: {selected_country}")
                    
                    # Admin1 selection
                    try:
                        country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', selected_country)).first()
                        country_code = country_feature.get('ADM0_CODE').getInfo()
                        
                        admin1_fc = get_admin_boundaries(1, country_code)
                        if admin1_fc is not None:
                            admin1_names = get_boundary_names(admin1_fc, 1)
                            selected_admin1 = st.selectbox(
                                "State/Province",
                                options=["Select state/province"] + admin1_names,
                                help="Choose a state or province",
                                key="admin1_select"
                            )
                            
                            if selected_admin1 and selected_admin1 != "Select state/province":
                                # Admin2 selection
                                try:
                                    admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', selected_admin1)).first()
                                    admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                                    
                                    admin2_fc = get_admin_boundaries(2, None, admin1_code)
                                    if admin2_fc is not None:
                                        admin2_names = get_boundary_names(admin2_fc, 2)
                                        selected_admin2 = st.selectbox(
                                            "Municipality",
                                            options=["Select municipality"] + admin2_names,
                                            help="Choose a municipality",
                                            key="admin2_select"
                                        )
                                except Exception as e:
                                    st.error(f"Error loading admin2: {str(e)}")
                    except Exception as e:
                        st.error(f"Error loading admin1: {str(e)}")
        except Exception as e:
            st.error(f"Error loading countries: {str(e)}")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Index selection - like screenshot
    st.markdown('<div class="form-label">Vegetation Index</div>', unsafe_allow_html=True)
    
    available_indices = [
        'NDVI', 'ARVI', 'ATSAVI', 'DVI', 'EVI', 'EVI2', 'GNDVI', 'MSAVI', 'MSI', 'MTVI', 'MTVI2',
        'NDTI', 'NDWI', 'OSAVI', 'RDVI', 'RI', 'RVI', 'SAVI', 'TVI', 'TSAVI', 'VARI', 'VIN', 'WDRVI',
        'GCVI', 'AWEI', 'MNDWI', 'WI', 'ANDWI', 'NDSI', 'nDDI', 'NBR', 'DBSI', 'SI', 'S3', 'BRI',
        'SSI', 'NDSI_Salinity', 'SRPI', 'MCARI', 'NDCI', 'PSSRb1', 'SIPI', 'PSRI', 'Chl_red_edge', 'MARI', 'NDMI'
    ]
    
    selected_indices = st.multiselect(
        "",
        options=available_indices,
        default=['NDVI'],
        help="Choose vegetation indices to analyze",
        key="indices_select",
        label_visibility="collapsed"
    )
    
    # Show description for selected index
    if selected_indices:
        index_descriptions = {
            'NDVI': 'Vegetation vigor',
            'EVI': 'Enhanced vegetation index',
            'SAVI': 'Soil-adjusted vegetation index',
            'NDWI': 'Water content'
        }
        for idx in selected_indices[:1]:  # Show for first selected
            desc = index_descriptions.get(idx, 'Vegetation index')
            st.markdown(f'<div style="color: #888; font-size: 0.875rem; margin-top: 0.5rem;">{desc}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Run analysis button
    if st.button("🚀 Run analysis", type="primary", key="run_analysis_main", use_container_width=True):
        if not selected_indices:
            st.error("Please select at least one vegetation index")
        else:
            with st.spinner("Running analysis..."):
                # Your analysis code here
                st.success("✅ Analysis completed!")
                st.session_state.analysis_results = {"mock": "data"}  # Replace with actual results
    
    st.markdown('<div class="panel-subtitle" style="margin-top: 1rem;">Analysis is simulated for the mockup.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # More options panel
    st.markdown('<div class="options-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><h3 class="panel-title">More options</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="form-label">Cloud max</div>', unsafe_allow_html=True)
        cloud_max = st.slider(
            "",
            min_value=0,
            max_value=100,
            value=20,
            key="cloud_max_slider",
            label_visibility="collapsed"
        )
        st.markdown(f'<div class="panel-subtitle">{cloud_max}%</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="form-label">Options</div>', unsafe_allow_html=True)
        apply_mask = st.checkbox("Apply mask", value=True, key="apply_mask")
        smooth_data = st.checkbox("Smooth data", value=True, key="smooth_data")
    
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN (Map) - matches screenshot layout
with st.container():
    st.markdown('<div class="clean-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header"><h3 class="panel-title">Map</h3></div>', unsafe_allow_html=True)
    
    # Map controls - like screenshot
    st.markdown("""
    <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <span class="status-badge">NDVI</span>
        <span class="status-badge">cloud ≤ 20%</span>
        <span class="status-badge">mask: on</span>
        <span class="status-badge">smooth: on</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Map placeholder - you can replace this with your actual map
    st.markdown("""
    <div class="map-container" style="height: 400px; display: flex; align-items: center; justify-content: center; color: #666;">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🗺️</div>
            <div style="font-size: 0.875rem; color: #888;">Draw / Upload area (visual placeholder)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Map controls at bottom
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a:
        st.button("Basemap", use_container_width=True)
    with col_b:
        st.button("Layers", use_container_width=True)
    with col_c:
        st.button("Draw", use_container_width=True)
    with col_d:
        st.button("Upload", use_container_width=True)
    with col_e:
        st.button("Center", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close two-col-layout

# Update the authentication section to match the clean style:
if not st.session_state.authenticated:
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; text-align: center;">
        <div class="clean-panel">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🔐</div>
            <h2 style="color: #ffffff; margin-bottom: 0.5rem;">KHISBA GIS</h2>
            <p style="color: #888; margin-bottom: 2rem;">Vegetation Analytics</p>
            
            <div style="margin-bottom: 1.5rem;">
                <div class="form-label">Password</div>
                <input type="password" placeholder="Enter admin password" style="
                    width: 100%;
                    padding: 12px;
                    background: #252525;
                    border: 1px solid #3a3a3a;
                    border-radius: 6px;
                    color: #e0e0e0;
                    font-size: 0.875rem;
                    margin-bottom: 1rem;
                ">
            </div>
            
            <button style="
                background: #00ff88;
                color: #000000;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 0.875rem;
                width: 100%;
                cursor: pointer;
            ">🔓 Sign In</button>
            
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #2a2a2a;">
                <div class="panel-subtitle">Demo Access</div>
                <div style="color: #888; font-size: 0.875rem; margin-top: 0.5rem;">
                    Use <strong>admin</strong> for password
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # You'll need to handle the actual password input with Streamlit components
    password = st.text_input("", type="password", placeholder="Enter admin password", label_visibility="collapsed", key="auth_pass")
    if st.button("🔓 Sign In", type="primary", use_container_width=True):
        if password == "admin":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid password")
    
    st.stop()
