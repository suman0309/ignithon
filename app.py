from flask import Flask, jsonify
from firebase_admin import credentials, firestore, initialize_app
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import os
from typing import Dict, List, Tuple, Optional

app = Flask(__name__)

# Initialize Firebase Admin SDK
# You can either use a service account key file or set environment variables
try:
    # Option 1: Using service account key file
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    initialize_app(cred)
except FileNotFoundError:
    # Option 2: Using environment variables (recommended for production)
    # Set these environment variables:
    # FIREBASE_PROJECT_ID=your-project-id
    # FIREBASE_PRIVATE_KEY_ID=your-private-key-id
    # FIREBASE_PRIVATE_KEY=your-private-key
    # FIREBASE_CLIENT_EMAIL=your-client-email
    # FIREBASE_CLIENT_ID=your-client-id
    # FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
    # FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
    # FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
    # FIREBASE_CLIENT_X509_CERT_URL=your-cert-url
    
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
    })
    initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Initialize geocoder for converting addresses to coordinates
geolocator = Nominatim(user_agent="xylemcscis_food_donation")

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
        # Fetch donors from Firestore
        donors_ref = db.collection('donations')
        donors_docs = donors_ref.stream()
        
        donors = []
        for doc in donors_docs:
            donor_data = doc.to_dict()
            donor_data['id'] = doc.id
            donors.append(donor_data)
        
        # Fetch NGOs from Firestore
        ngos_ref = db.collection('ngoRequests')
        ngos_docs = ngos_ref.stream()
        
        ngos = []
        for doc in ngos_docs:
            ngo_data = doc.to_dict()
            ngo_data['id'] = doc.id
            ngos.append(ngo_data)
        
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
            'matches': matches
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/donors', methods=['GET'])
def get_donors():
    """Get all donors from Firestore."""
    try:
        donors_ref = db.collection('donations')
        donors_docs = donors_ref.stream()
        
        donors = []
        for doc in donors_docs:
            donor_data = doc.to_dict()
            donor_data['id'] = doc.id
            donors.append(donor_data)
        
        return jsonify({
            'success': True,
            'count': len(donors),
            'donors': donors
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ngos', methods=['GET'])
def get_ngos():
    """Get all NGOs from Firestore."""
    try:
        ngos_ref = db.collection('ngoRequests')
        ngos_docs = ngos_ref.stream()
        
        ngos = []
        for doc in ngos_docs:
            ngo_data = doc.to_dict()
            ngo_data['id'] = doc.id
            ngos.append(ngo_data)
        
        return jsonify({
            'success': True,
            'count': len(ngos),
            'ngos': ngos
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
        'service': 'XylemCSCIS Food Donation Backend',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
