from flask import Flask, jsonify
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Dict, List, Tuple, Optional
import json

app = Flask(__name__)

# Initialize geocoder for converting addresses to coordinates
geolocator = Nominatim(user_agent="xylemcscis_food_donation")

# Sample data for testing (simulating Firestore data)
SAMPLE_DONORS = [
    {
        "id": "donor_1",
        "foodType": "Rice",
        "quantity": "10 kg",
        "expiryTime": 48,
        "location": "New York, NY",
        "timestamp": "2023-12-01T10:30:00Z"
    },
    {
        "id": "donor_2", 
        "foodType": "Bread",
        "quantity": "20 loaves",
        "expiryTime": 24,
        "location": "Brooklyn, NY",
        "timestamp": "2023-12-01T11:15:00Z"
    },
    {
        "id": "donor_3",
        "foodType": "Vegetables",
        "quantity": "5 kg",
        "expiryTime": 72,
        "location": "Queens, NY",
        "timestamp": "2023-12-01T09:45:00Z"
    }
]

SAMPLE_NGOS = [
    {
        "id": "ngo_1",
        "ngoName": "Food Bank NYC",
        "foodNeeded": "Rice, Bread, Vegetables",
        "location": "Manhattan, NY",
        "timestamp": "2023-12-01T08:30:00Z"
    },
    {
        "id": "ngo_2",
        "ngoName": "Community Kitchen",
        "foodNeeded": "Bread, Vegetables",
        "location": "Bronx, NY", 
        "timestamp": "2023-12-01T09:00:00Z"
    },
    {
        "id": "ngo_3",
        "ngoName": "Homeless Shelter",
        "foodNeeded": "Rice, Bread",
        "location": "Staten Island, NY",
        "timestamp": "2023-12-01T07:45:00Z"
    }
]

def get_coordinates(location: str) -> Optional[Tuple[float, float]]:
    """
    Convert location string to latitude and longitude coordinates.
    
    Args:
        location (str): Location string (e.g., "New York, NY")
        
    Returns:
        Optional[Tuple[float, float]]: (latitude, longitude) or None if geocoding fails
    """
    try:
        location_data = geolocator.geocode(location)
        if location_data:
            return (location_data.latitude, location_data.longitude)
        return None
    except Exception as e:
        print(f"Error geocoding location '{location}': {e}")
        return None

def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate distance between two coordinates using geodesic distance.
    
    Args:
        coord1 (Tuple[float, float]): First coordinate (lat, lon)
        coord2 (Tuple[float, float]): Second coordinate (lat, lon)
        
    Returns:
        float: Distance in kilometers
    """
    return geodesic(coord1, coord2).kilometers

def find_closest_ngo(donor_coords: Tuple[float, float], ngo_locations: List[Dict]) -> Optional[Dict]:
    """
    Find the closest NGO to a donor based on coordinates.
    
    Args:
        donor_coords (Tuple[float, float]): Donor's coordinates
        ngo_locations (List[Dict]): List of NGOs with their coordinates
        
    Returns:
        Optional[Dict]: Closest NGO data or None if no valid NGOs
    """
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

@app.route('/api/matches', methods=['GET'])
def get_donor_ngo_matches():
    """
    Main endpoint to get donor-NGO matches.
    
    Returns:
        JSON response with donor → matched NGO data
    """
    try:
        # Use sample data instead of Firestore
        donors = SAMPLE_DONORS.copy()
        ngos = SAMPLE_NGOS.copy()
        
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
            'note': 'Using sample data - Firebase not configured'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/donors', methods=['GET'])
def get_donors():
    """Get all donors (sample data)."""
    try:
        return jsonify({
            'success': True,
            'count': len(SAMPLE_DONORS),
            'donors': SAMPLE_DONORS,
            'note': 'Using sample data - Firebase not configured'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ngos', methods=['GET'])
def get_ngos():
    """Get all NGOs (sample data)."""
    try:
        return jsonify({
            'success': True,
            'count': len(SAMPLE_NGOS),
            'ngos': SAMPLE_NGOS,
            'note': 'Using sample data - Firebase not configured'
        })
        
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
        'note': 'Running with sample data - Firebase not configured'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        'message': 'XylemCSCIS Food Donation Backend API',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/matches': 'Get donor-NGO matches based on location',
            'GET /api/donors': 'Get all donors',
            'GET /api/ngos': 'Get all NGOs', 
            'GET /api/health': 'Health check',
            'GET /': 'This help message'
        },
        'note': 'Currently running with sample data. Configure Firebase for production use.'
    })

if __name__ == '__main__':
    print("🚀 Starting XylemCSCIS Food Donation Backend...")
    print("📍 Demo mode - using sample data")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 API docs available at: http://localhost:5000/")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("🎯 Matches endpoint: http://localhost:5000/api/matches")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
