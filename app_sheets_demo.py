from flask import Flask, jsonify, request
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

app = Flask(__name__)

# Initialize geocoder for converting addresses to coordinates
geolocator = Nominatim(user_agent="xylemcscis_food_donation")

# In-memory storage for demo (simulates Google Sheets)
DEMO_DONORS = []
DEMO_NGOS = []

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

def add_donor_demo(donor_data: Dict) -> bool:
    """Add a new donor to demo storage."""
    try:
        # Generate unique ID
        donor_id = f"donor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create donor record
        donor = {
            'id': donor_id,
            'foodType': donor_data.get('foodType', ''),
            'quantity': donor_data.get('quantity', ''),
            'expiryTime': donor_data.get('expiryTime', 0),
            'location': donor_data.get('location', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        DEMO_DONORS.append(donor)
        print(f"✅ Added donor: {donor_id}")
        return True
    except Exception as e:
        print(f"Error adding donor: {e}")
        return False

def add_ngo_demo(ngo_data: Dict) -> bool:
    """Add a new NGO to demo storage."""
    try:
        # Generate unique ID
        ngo_id = f"ngo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create NGO record
        ngo = {
            'id': ngo_id,
            'ngoName': ngo_data.get('ngoName', ''),
            'foodNeeded': ngo_data.get('foodNeeded', ''),
            'location': ngo_data.get('location', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        DEMO_NGOS.append(ngo)
        print(f"✅ Added NGO: {ngo_id}")
        return True
    except Exception as e:
        print(f"Error adding NGO: {e}")
        return False

# API Endpoints

@app.route('/api/matches', methods=['GET'])
def get_donor_ngo_matches():
    """Main endpoint to get donor-NGO matches."""
    try:
        # Get data from demo storage
        donors = DEMO_DONORS.copy()
        ngos = DEMO_NGOS.copy()
        
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
            'database': 'Demo Mode (In-Memory)',
            'note': 'Data is stored in memory and will be lost when server restarts'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/donors', methods=['GET'])
def get_donors():
    """Get all donors from demo storage."""
    try:
        return jsonify({
            'success': True,
            'count': len(DEMO_DONORS),
            'donors': DEMO_DONORS,
            'database': 'Demo Mode (In-Memory)'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ngos', methods=['GET'])
def get_ngos():
    """Get all NGOs from demo storage."""
    try:
        return jsonify({
            'success': True,
            'count': len(DEMO_NGOS),
            'ngos': DEMO_NGOS,
            'database': 'Demo Mode (In-Memory)'
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
        
        # Add donor to demo storage
        success = add_donor_demo(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Donor added successfully',
                'database': 'Demo Mode (In-Memory)'
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
        
        # Add NGO to demo storage
        success = add_ngo_demo(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'NGO added successfully',
                'database': 'Demo Mode (In-Memory)'
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
    return jsonify({
        'status': 'healthy',
        'service': 'XylemCSCIS Food Donation Backend (Demo Mode)',
        'version': '1.0.0',
        'database': 'Demo Mode (In-Memory)',
        'sheets_status': 'demo_mode'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        'message': 'XylemCSCIS Food Donation Backend API (Demo Mode)',
        'version': '1.0.0',
        'database': 'Demo Mode (In-Memory)',
        'endpoints': {
            'GET /api/matches': 'Get donor-NGO matches based on location',
            'GET /api/donors': 'Get all donors',
            'POST /api/donors': 'Add new donor',
            'GET /api/ngos': 'Get all NGOs',
            'POST /api/ngos': 'Add new NGO',
            'GET /api/health': 'Health check',
            'GET /': 'This help message'
        },
        'demo_mode': {
            'note': 'This is a demo version using in-memory storage',
            'data_persistence': 'Data will be lost when server restarts',
            'setup_required': 'No Google Sheets setup required for demo'
        }
    })

if __name__ == '__main__':
    print("🚀 Starting XylemCSCIS Food Donation Backend (Demo Mode)...")
    print("📊 Database: Demo Mode (In-Memory)")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API docs available at: http://localhost:5000/")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("🎯 Matches endpoint: http://localhost:5000/api/matches")
    print("📝 Add donor: POST http://localhost:5000/api/donors")
    print("📝 Add NGO: POST http://localhost:5000/api/ngos")
    print("\n💡 Demo Mode: Data is stored in memory and will be lost on restart")
    print("🔧 For Google Sheets integration, use app_sheets.py with proper setup")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
