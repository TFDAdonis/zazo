from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import tempfile
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import ee
import pandas as pd
import traceback
from pydantic import BaseModel

# Pydantic models for request/response
class AuthRequest(BaseModel):
    password: str

class DateRange(BaseModel):
    start_date: str
    end_date: str

class AnalysisRequest(BaseModel):
    country: Optional[str] = None
    admin1: Optional[str] = None
    admin2: Optional[str] = None
    start_date: str
    end_date: str
    cloud_cover: int = 20
    collection_choice: str = "Sentinel-2"
    indices: List[str]
    geometry: Optional[Dict[str, Any]] = None

class GeometryRequest(BaseModel):
    country: Optional[str] = None
    admin1: Optional[str] = None
    admin2: Optional[str] = None

app = FastAPI(title="Khisba GIS API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
security = HTTPBearer()
VALID_PASSWORD = "admin"

# Store initialized state
ee_initialized = False

# Initialize Earth Engine
def initialize_earth_engine():
    """Initialize Earth Engine with service account"""
    global ee_initialized
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
        ee_initialized = True
        return True
    except Exception as e:
        print(f"Earth Engine initialization failed: {str(e)}")
        return False

# Authentication endpoint
@app.post("/api/auth/login")
async def login(auth: AuthRequest):
    if auth.password == VALID_PASSWORD:
        return {"success": True, "message": "Authentication successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")

# Check Earth Engine status
@app.get("/api/ee/status")
async def get_ee_status():
    if not ee_initialized:
        success = initialize_earth_engine()
        return {"initialized": success}
    return {"initialized": True}

# Get administrative boundaries
@app.get("/api/geography/countries")
async def get_countries():
    try:
        countries_fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
        countries = countries_fc.aggregate_array('ADM0_NAME').distinct().getInfo()
        return {"countries": sorted(countries)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/geography/admin1")
async def get_admin1(country: str):
    try:
        countries_fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
        country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', country)).first()
        country_code = country_feature.get('ADM0_CODE').getInfo()
        
        admin1_fc = ee.FeatureCollection("FAO/GAUL/2015/level1")\
            .filter(ee.Filter.eq('ADM0_CODE', country_code))
        
        admin1_names = admin1_fc.aggregate_array('ADM1_NAME').distinct().getInfo()
        return {"admin1": sorted(admin1_names)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/geography/admin2")
async def get_admin2(country: str, admin1: str):
    try:
        countries_fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
        country_feature = countries_fc.filter(ee.Filter.eq('ADM0_NAME', country)).first()
        country_code = country_feature.get('ADM0_CODE').getInfo()
        
        admin1_fc = ee.FeatureCollection("FAO/GAUL/2015/level1")\
            .filter(ee.Filter.eq('ADM0_CODE', country_code))
        
        admin1_feature = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', admin1)).first()
        admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
        
        admin2_fc = ee.FeatureCollection("FAO/GAUL/2015/level2")\
            .filter(ee.Filter.eq('ADM1_CODE', admin1_code))
        
        admin2_names = admin2_fc.aggregate_array('ADM2_NAME').distinct().getInfo()
        return {"admin2": sorted(admin2_names)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get geometry bounds for map
@app.post("/api/geography/geometry")
async def get_geometry(request: GeometryRequest):
    try:
        countries_fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
        
        if request.country:
            geometry = countries_fc.filter(ee.Filter.eq('ADM0_NAME', request.country))
            
            if request.admin1:
                country_feature = geometry.first()
                country_code = country_feature.get('ADM0_CODE').getInfo()
                
                admin1_fc = ee.FeatureCollection("FAO/GAUL/2015/level1")\
                    .filter(ee.Filter.eq('ADM0_CODE', country_code))
                
                geometry = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', request.admin1))
                
                if request.admin2:
                    admin1_feature = geometry.first()
                    admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                    
                    admin2_fc = ee.FeatureCollection("FAO/GAUL/2015/level2")\
                        .filter(ee.Filter.eq('ADM1_CODE', admin1_code))
                    
                    geometry = admin2_fc.filter(ee.Filter.eq('ADM2_NAME', request.admin2))
        
        bounds = geometry.geometry().bounds().getInfo()
        coords = bounds['coordinates'][0]
        
        # Calculate center
        lats = [coord[1] for coord in coords]
        lons = [coord[0] for coord in coords]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        return {
            "bounds": bounds,
            "center": {"lat": center_lat, "lon": center_lon},
            "area_name": f"{request.admin2 or request.admin1 or request.country}",
            "area_level": "Country" if not request.admin1 else "State/Province" if not request.admin2 else "Municipality"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run vegetation analysis
@app.post("/api/analysis/run")
async def run_analysis(request: AnalysisRequest):
    try:
        # Import your existing vegetation analysis functions
        from vegetation_indices import mask_clouds, add_vegetation_indices
        
        # Get geometry based on selection
        countries_fc = ee.FeatureCollection("FAO/GAUL/2015/level0")
        
        if request.country:
            geometry = countries_fc.filter(ee.Filter.eq('ADM0_NAME', request.country))
            
            if request.admin1:
                country_feature = geometry.first()
                country_code = country_feature.get('ADM0_CODE').getInfo()
                
                admin1_fc = ee.FeatureCollection("FAO/GAUL/2015/level1")\
                    .filter(ee.Filter.eq('ADM0_CODE', country_code))
                
                geometry = admin1_fc.filter(ee.Filter.eq('ADM1_NAME', request.admin1))
                
                if request.admin2:
                    admin1_feature = geometry.first()
                    admin1_code = admin1_feature.get('ADM1_CODE').getInfo()
                    
                    admin2_fc = ee.FeatureCollection("FAO/GAUL/2015/level2")\
                        .filter(ee.Filter.eq('ADM1_CODE', admin1_code))
                    
                    geometry = admin2_fc.filter(ee.Filter.eq('ADM2_NAME', request.admin2))
        
        # Define collection
        if request.collection_choice == "Sentinel-2":
            collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        else:
            collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
        
        # Filter collection
        filtered_collection = (collection
            .filterDate(request.start_date, request.end_date)
            .filterBounds(geometry)
            .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', request.cloud_cover))
        )
        
        # Process collection
        if request.collection_choice == "Sentinel-2":
            processed_collection = (filtered_collection
                .map(mask_clouds)
                .map(add_vegetation_indices)
            )
        else:
            processed_collection = filtered_collection.map(add_vegetation_indices)
        
        # Calculate time series
        results = {}
        for index in request.indices:
            try:
                def add_date_and_reduce(image):
                    reduced = image.select(index).reduceRegion(
                        reducer=ee.Reducer.mean(),
                        geometry=geometry.geometry(),
                        scale=30,
                        maxPixels=1e9
                    )
                    return ee.Feature(None, reduced.set('date', image.date().format()))
                
                time_series = processed_collection.map(add_date_and_reduce)
                time_series_list = time_series.getInfo()
                
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
                print(f"Error calculating {index}: {str(e)}")
                results[index] = {'dates': [], 'values': []}
        
        return {
            "success": True,
            "results": results,
            "metadata": {
                "area_name": request.admin2 or request.admin1 or request.country,
                "date_range": f"{request.start_date} to {request.end_date}",
                "collection": request.collection_choice,
                "indices_analyzed": request.indices
            }
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Get available vegetation indices
@app.get("/api/indices/list")
async def get_available_indices():
    indices = [
        'NDVI', 'ARVI', 'ATSAVI', 'DVI', 'EVI', 'EVI2', 'GNDVI', 'MSAVI', 'MSI', 'MTVI', 'MTVI2',
        'NDTI', 'NDWI', 'OSAVI', 'RDVI', 'RI', 'RVI', 'SAVI', 'TVI', 'TSAVI', 'VARI', 'VIN', 'WDRVI',
        'GCVI', 'AWEI', 'MNDWI', 'WI', 'ANDWI', 'NDSI', 'nDDI', 'NBR', 'DBSI', 'SI', 'S3', 'BRI',
        'SSI', 'NDSI_Salinity', 'SRPI', 'MCARI', 'NDCI', 'PSSRb1', 'SIPI', 'PSRI', 'Chl_red_edge', 'MARI', 'NDMI'
    ]
    return {"indices": indices}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
