# XylemCSCIS Food Donation Backend

A Flask backend that connects to Firebase Firestore and matches food donors with the closest NGOs based on location using geopy for distance calculations.

## Features

- 🔥 **Firebase Firestore Integration**: Connects to your Firebase project
- 📍 **Location-based Matching**: Uses geopy to calculate distances between donors and NGOs
- 🎯 **Smart Matching Algorithm**: Finds the closest NGO for each donor
- 📊 **RESTful API**: Clean JSON responses with comprehensive data
- 🛡️ **Error Handling**: Robust error handling and validation
- 🔍 **Health Check**: Built-in health monitoring endpoint

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Firebase Configuration

You have two options for Firebase authentication:

#### Option A: Service Account Key File (Development)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Navigate to Project Settings → Service Accounts
3. Click "Generate New Private Key"
4. Save the JSON file as `serviceAccountKey.json` in your project root
5. Update the path in `app.py`:

```python
cred = credentials.Certificate("path/to/serviceAccountKey.json")
```

#### Option B: Environment Variables (Production - Recommended)

Set these environment variables:

```bash
export FIREBASE_PROJECT_ID="your-project-id"
export FIREBASE_PRIVATE_KEY_ID="your-private-key-id"
export FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
export FIREBASE_CLIENT_EMAIL="your-service-account@your-project.iam.gserviceaccount.com"
export FIREBASE_CLIENT_ID="your-client-id"
export FIREBASE_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
export FIREBASE_TOKEN_URI="https://oauth2.googleapis.com/token"
export FIREBASE_AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
export FIREBASE_CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Get Donor-NGO Matches
**GET** `/api/matches`

Returns matched donors with their closest NGOs based on location.

**Response:**
```json
{
  "success": true,
  "total_donors": 5,
  "total_ngos": 3,
  "successful_matches": 4,
  "matches": [
    {
      "donor": {
        "id": "donor_id_1",
        "food_type": "Rice",
        "quantity": "10 kg",
        "expiry_time_hours": 48,
        "location": "New York, NY",
        "coordinates": [40.7128, -74.0060],
        "timestamp": "2023-12-01T10:30:00Z"
      },
      "matched_ngo": {
        "id": "ngo_id_2",
        "ngo_name": "Food Bank NYC",
        "food_needed": "Rice, Bread",
        "location": "Brooklyn, NY",
        "coordinates": [40.6782, -73.9442],
        "distance_km": 8.45,
        "timestamp": "2023-12-01T09:15:00Z"
      }
    }
  ]
}
```

### 2. Get All Donors
**GET** `/api/donors`

Returns all donor entries from Firestore.

**Response:**
```json
{
  "success": true,
  "count": 5,
  "donors": [
    {
      "id": "donor_id_1",
      "foodType": "Rice",
      "quantity": "10 kg",
      "expiryTime": 48,
      "location": "New York, NY",
      "timestamp": "2023-12-01T10:30:00Z"
    }
  ]
}
```

### 3. Get All NGOs
**GET** `/api/ngos`

Returns all NGO entries from Firestore.

**Response:**
```json
{
  "success": true,
  "count": 3,
  "ngos": [
    {
      "id": "ngo_id_1",
      "ngoName": "Food Bank NYC",
      "foodNeeded": "Rice, Bread",
      "location": "Brooklyn, NY",
      "timestamp": "2023-12-01T09:15:00Z"
    }
  ]
}
```

### 4. Health Check
**GET** `/api/health`

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "XylemCSCIS Food Donation Backend",
  "version": "1.0.0"
}
```

## How It Works

### 1. Data Fetching
- Fetches all donors from the `donations` collection
- Fetches all NGOs from the `ngoRequests` collection

### 2. Geocoding
- Converts location strings to latitude/longitude coordinates using Nominatim
- Handles geocoding errors gracefully

### 3. Distance Calculation
- Uses geodesic distance (Haversine formula) for accurate distance calculation
- Calculates distances in kilometers

### 4. Matching Algorithm
- For each donor, finds the NGO with the minimum distance
- Returns comprehensive match data including distance information

## Error Handling

The API includes robust error handling:

- **Geocoding Failures**: Skips entries with invalid locations
- **Firebase Errors**: Returns appropriate error responses
- **Network Issues**: Handles timeouts and connection problems
- **Invalid Data**: Validates input data before processing

## Example Usage

### Using curl

```bash
# Get all matches
curl http://localhost:5000/api/matches

# Get all donors
curl http://localhost:5000/api/donors

# Get all NGOs
curl http://localhost:5000/api/ngos

# Health check
curl http://localhost:5000/api/health
```

### Using Python requests

```python
import requests

# Get matches
response = requests.get('http://localhost:5000/api/matches')
matches = response.json()

# Get donors
response = requests.get('http://localhost:5000/api/donors')
donors = response.json()

# Get NGOs
response = requests.get('http://localhost:5000/api/ngos')
ngos = response.json()
```

## Performance Considerations

- **Geocoding Rate Limits**: Nominatim has rate limits (1 request per second)
- **Caching**: Consider implementing caching for geocoded coordinates
- **Batch Processing**: For large datasets, consider batch processing
- **Database Indexing**: Ensure proper Firestore indexing for queries

## Security Notes

- Keep your Firebase service account key secure
- Use environment variables in production
- Implement proper authentication for production use
- Consider rate limiting for API endpoints

## Troubleshooting

### Common Issues

1. **Firebase Connection Error**
   - Verify your service account credentials
   - Check your Firebase project ID
   - Ensure Firestore is enabled in your project

2. **Geocoding Failures**
   - Check location string format
   - Verify internet connection
   - Consider using more specific location strings

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify virtual environment setup

### Debug Mode

Run with debug mode for detailed error messages:

```bash
export FLASK_ENV=development
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the XylemCSCIS Food Donation Platform.
