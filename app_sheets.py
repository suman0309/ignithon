from flask import Flask, jsonify, request
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Dict, List, Tuple, Optional
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__)

# Google Sheets API setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Initialize Google Sheets client
def init_google_sheets():
    """Initialize Google Sheets client with credentials."""
    try:
        # Option 1: Using service account key file
        creds = Credentials.from_service_account_file(
            'google-sheets-credentials.json', 
            scopes=SCOPES
        )
    except FileNotFoundError:
        # Option 2: Using environment variables
        creds = Credentials.from_service_account_info({
            "type": "service_account",
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
        }, scopes=SCOPES)
    
    client = gspread.authorize(creds)
    return client

# Initialize sheets client
try:
    sheets_client = init_google_sheets()
    print("✅ Google Sheets client initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Google Sheets: {e}")
    sheets_client = None

# Sheet names (you can change these)
DONORS_SHEET_NAME = "Donors"
NGOS_SHEET_NAME = "NGOs"

def get_or_create_sheet(sheet_name: str) -> gspread.Worksheet:
    """Get or create a Google Sheet with the given name."""
    try:
        # Try to open existing sheet
        sheet = sheets_client.open(sheet_name)
        worksheet = sheet.sheet1
    except gspread.SpreadsheetNotFound:
        # Create new sheet if it doesn't exist
        sheet = sheets_client.create(sheet_name)
        worksheet = sheet.sheet1
        
        # Set up headers based on sheet type
        if sheet_name == DONORS_SHEET_NAME:
            headers = ['ID', 'Food Type', 'Quantity', 'Expiry Time (hours)', 'Location', 'Timestamp']
        elif sheet_name == NGOS_SHEET_NAME:
            headers = ['ID', 'NGO Name', 'Food Needed', 'Location', 'Timestamp']
        else:
            headers = ['ID', 'Data', 'Timestamp']
        
        worksheet.append_row(headers)
        print(f"📊 Created new sheet: {sheet_name}")
    
    return worksheet

def get_all_donors() -> List[Dict]:
    """Get all donors from Google Sheets."""
    try:
        worksheet = get_or_create_sheet(DONORS_SHEET_NAME)
        records = worksheet.get_all_records()
        
        donors = []
        for record in records:
            if record.get('ID'):  # Skip empty rows
                donors.append({
                    'id': record['ID'],
                    'foodType': record.get('Food Type', ''),
                    'quantity': record.get('Quantity', ''),
                    'expiryTime': int(record.get('Expiry Time (hours)', 0)),
                    'location': record.get('Location', ''),
                    'timestamp': record.get('Timestamp', '')
                })
        
        return donors
    except Exception as e:
        print(f"Error getting donors: {e}")
        return []

def get_all_ngos() -> List[Dict]:
    """Get all NGOs from Google Sheets."""
    try:
        worksheet = get_or_create_sheet(NGOS_SHEET_NAME)
        records = worksheet.get_all_records()
        
        ngos = []
        for record in records:
            if record.get('ID'):  # Skip empty rows
                ngos.append({
                    'id': record['ID'],
                    'ngoName': record.get('NGO Name', ''),
                    'foodNeeded': record.get('Food Needed', ''),
                    'location': record.get('Location', ''),
                    'timestamp': record.get('Timestamp', '')
                })
        
        return ngos
    except Exception as e:
        print(f"Error getting NGOs: {e}")
        return []

def add_donor(donor_data: Dict) -> bool:
    """Add a new donor to Google Sheets."""
    try:
        worksheet = get_or_create_sheet(DONORS_SHEET_NAME)
        
        # Generate unique ID
        donor_id = f"donor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare row data
        row = [
            donor_id,
            donor_data.get('foodType', ''),
            donor_data.get('quantity', ''),
            donor_data.get('expiryTime', 0),
            donor_data.get('location', ''),
            datetime.now().isoformat()
        ]
        
        worksheet.append_row(row)
        print(f"✅ Added donor: {donor_id}")
        return True
    except Exception as e:
        print(f"Error adding donor: {e}")
        return False

def add_ngo(ngo_data: Dict) -> bool:
    """Add a new NGO to Google Sheets."""
    try:
        worksheet = get_or_create_sheet(NGOS_SHEET_NAME)
        
        # Generate unique ID
        ngo_id = f"ngo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare row data
        row = [
            ngo_id,
            ngo_data.get('ngoName', ''),
            ngo_data.get('foodNeeded', ''),
            ngo_data.get('location', ''),
            datetime.now().isoformat()
        ]
        
        worksheet.append_row(row)
        print(f"✅ Added NGO: {ngo_id}")
        return True
    except Exception as e:
        print(f"Error adding NGO: {e}")
        return False

# Initialize geocoder for converting addresses to coordinates
geolocator = Nominatim(user_agent="xylemcscis_food_donation")

def get_coordinates(location: str) -> Optional[Tuple[float, float]]:
    """Convert location string to latitude and longitude coordinates."""
    try:
        location_data = geolocator.geocode(location)
        if location_data:
            return (location_data.latitude, location_data.longitude)
        return None
    except Exception as e:
        print(f"Error geocoding location '{location}': {e}")
        return None

def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Calculate distance between two coordinates using geodesic distance."""
    return geodesic(coord1, coord2).kilometers

def find_closest_ngo(donor_coords: Tuple[float, float], ngo_locations: List[Dict]) -> Optional[Dict]:
    """Find the closest NGO to a donor based on coordinates."""
    closest_ngo = None
    min_distance = float('inf')
    
    for ngo in ngo_locations:
        if ngo.get('coordinates'):
            distance = calculate_distance(donor_coords, ngo['coordinates'])
            if distance < min_distance:
                min_distance = distance
                closest_ngo = ngo.copy()
                closest_ngo['distance_km'] = round(distance, 2)
    
    return closest_ngo

# API Endpoints

@app.route('/api/matches', methods=['GET'])
def get_donor_ngo_matches():
    """Main endpoint to get donor-NGO matches."""
    try:
        # Get data from Google Sheets
        donors = get_all_donors()
        ngos = get_all_ngos()
        
        # Get coordinates for all NGOs
        ngo_locations = []
        for ngo in ngos:
            location = ngo.get('location', '')
            if location:
                coords = get_coordinates(location)
                if coords:
                    ngo['coordinates'] = coords
                    ngo_locations.append(ngo)
        
        # Match donors with closest NGOs
        matches = []
        for donor in donors:
            donor_location = donor.get('location', '')
            if donor_location:
                donor_coords = get_coordinates(donor_location)
                if donor_coords:
                    closest_ngo = find_closest_ngo(donor_coords, ngo_locations)
                    if closest_ngo:
                        match = {
                            'donor': {
                                'id': donor['id'],
                                'food_type': donor.get('foodType', ''),
                                'quantity': donor.get('quantity', ''),
                                'expiry_time_hours': donor.get('expiryTime', 0),
                                'location': donor_location,
                                'coordinates': donor_coords,
                                'timestamp': donor.get('timestamp', '')
                            },
                            'matched_ngo': {
                                'id': closest_ngo['id'],
                                'ngo_name': closest_ngo.get('ngoName', ''),
                                'food_needed': closest_ngo.get('foodNeeded', ''),
                                'location': closest_ngo.get('location', ''),
                                'coordinates': closest_ngo['coordinates'],
                                'distance_km': closest_ngo['distance_km'],
                                'timestamp': closest_ngo.get('timestamp', '')
                            }
                        }
                        matches.append(match)
        
        return jsonify({
            'success': True,
            'total_donors': len(donors),
            'total_ngos': len(ngos),
            'successful_matches': len(matches),
            'matches': matches,
            'database': 'Google Sheets'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/donors', methods=['GET'])
def get_donors():
    """Get all donors from Google Sheets."""
    try:
        donors = get_all_donors()
        return jsonify({
            'success': True,
            'count': len(donors),
            'donors': donors,
            'database': 'Google Sheets'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ngos', methods=['GET'])
def get_ngos():
    """Get all NGOs from Google Sheets."""
    try:
        ngos = get_all_ngos()
        return jsonify({
            'success': True,
            'count': len(ngos),
            'ngos': ngos,
            'database': 'Google Sheets'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/donors', methods=['POST'])
def add_donor_endpoint():
    """Add a new donor via API."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['foodType', 'quantity', 'expiryTime', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Add donor to Google Sheets
        success = add_donor(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Donor added successfully',
                'database': 'Google Sheets'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add donor'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ngos', methods=['POST'])
def add_ngo_endpoint():
    """Add a new NGO via API."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['ngoName', 'foodNeeded', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Add NGO to Google Sheets
        success = add_ngo(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'NGO added successfully',
                'database': 'Google Sheets'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add NGO'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    sheets_status = "connected" if sheets_client else "disconnected"
    
    return jsonify({
        'status': 'healthy',
        'service': 'XylemCSCIS Food Donation Backend (Google Sheets)',
        'version': '1.0.0',
        'database': 'Google Sheets',
        'sheets_status': sheets_status
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        'message': 'XylemCSCIS Food Donation Backend API (Google Sheets)',
        'version': '1.0.0',
        'database': 'Google Sheets',
        'endpoints': {
            'GET /api/matches': 'Get donor-NGO matches based on location',
            'GET /api/donors': 'Get all donors',
            'POST /api/donors': 'Add new donor',
            'GET /api/ngos': 'Get all NGOs',
            'POST /api/ngos': 'Add new NGO',
            'GET /api/health': 'Health check',
            'GET /': 'This help message'
        },
        'sheets': {
            'donors_sheet': DONORS_SHEET_NAME,
            'ngos_sheet': NGOS_SHEET_NAME
        }
    })

if __name__ == '__main__':
    print("🚀 Starting XylemCSCIS Food Donation Backend (Google Sheets)...")
    print("📊 Database: Google Sheets")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API docs available at: http://localhost:5000/")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("🎯 Matches endpoint: http://localhost:5000/api/matches")
    print("📝 Add donor: POST http://localhost:5000/api/donors")
    print("📝 Add NGO: POST http://localhost:5000/api/ngos")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
