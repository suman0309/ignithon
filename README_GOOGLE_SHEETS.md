# 🍽️🏢 XylemCSCIS Food Donation Platform - Google Sheets Integration

A complete food donation platform that connects donors with NGOs using Google Sheets as the database and Flask as the backend API.

## 🚀 Features

### ✅ **Complete Backend API**
- **Flask REST API** with location-based matching
- **Google Sheets Integration** for data storage
- **Geopy Integration** for distance calculations
- **Real-time matching** between donors and NGOs

### ✅ **Smart Matching Algorithm**
- **Haversine Distance** calculation using geopy
- **Automatic geocoding** of location strings
- **Closest NGO matching** for each donor
- **Distance tracking** in kilometers

### ✅ **Easy Data Management**
- **Google Sheets** as database (no setup required)
- **Real-time collaboration** on data
- **Export capabilities** to CSV/Excel
- **Automatic backup** via Google Drive

## 📁 Project Structure

```
HACKATHON -IGNITHON/
├── index.html              # Frontend with login and forms
├── styles.css              # Styling and animations
├── script.js               # Frontend JavaScript (updated for API)
├── app_sheets.py           # Flask backend with Google Sheets
├── app_sheets_demo.py      # Demo version (in-memory storage)
├── requirements.txt        # Python dependencies
├── GOOGLE_SHEETS_SETUP.md  # Detailed setup guide
└── README_GOOGLE_SHEETS.md # This file
```

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Run Demo Version (No Setup Required)**
```bash
python app_sheets_demo.py
```

### 3. **Test the API**
```bash
# Health check
curl http://localhost:5000/api/health

# Add a donor
curl -X POST http://localhost:5000/api/donors \
  -H "Content-Type: application/json" \
  -d '{"foodType": "Rice", "quantity": "10 kg", "expiryTime": 48, "location": "New York, NY"}'

# Add an NGO
curl -X POST http://localhost:5000/api/ngos \
  -H "Content-Type: application/json" \
  -d '{"ngoName": "Food Bank NYC", "foodNeeded": "Rice, Bread", "location": "Manhattan, NY"}'

# Get matches
curl http://localhost:5000/api/matches
```

### 4. **Open Frontend**
Open `index.html` in your browser and start using the platform!

## 📡 API Endpoints

### **GET Endpoints**
- `GET /api/health` - Health check
- `GET /api/donors` - Get all donors
- `GET /api/ngos` - Get all NGOs
- `GET /api/matches` - Get donor-NGO matches

### **POST Endpoints**
- `POST /api/donors` - Add new donor
- `POST /api/ngos` - Add new NGO

## 🔧 Google Sheets Setup (Optional)

For production use with Google Sheets:

1. **Follow the setup guide**: `GOOGLE_SHEETS_SETUP.md`
2. **Get Google Cloud credentials**
3. **Run the full version**: `python app_sheets.py`

## 📊 Data Structure

### **Donor Data**
```json
{
  "foodType": "Rice",
  "quantity": "10 kg",
  "expiryTime": 48,
  "location": "New York, NY"
}
```

### **NGO Data**
```json
{
  "ngoName": "Food Bank NYC",
  "foodNeeded": "Rice, Bread, Vegetables",
  "location": "Manhattan, NY"
}
```

### **Match Result**
```json
{
  "donor": {
    "id": "donor_20231201_103000",
    "food_type": "Rice",
    "quantity": "10 kg",
    "location": "New York, NY",
    "coordinates": [40.7127281, -74.0060152]
  },
  "matched_ngo": {
    "id": "ngo_20231201_083000",
    "ngo_name": "Food Bank NYC",
    "food_needed": "Rice, Bread, Vegetables",
    "location": "Manhattan, NY",
    "coordinates": [40.7896239, -73.9598939],
    "distance_km": 9.39
  }
}
```

## 🎯 How It Works

### **1. User Interface**
- **Login page** with role selection (Donor/NGO)
- **Responsive forms** for data entry
- **Real-time feedback** and success messages

### **2. Backend Processing**
- **Form validation** and data sanitization
- **Geocoding** of location strings to coordinates
- **Distance calculation** using Haversine formula
- **Smart matching** algorithm

### **3. Data Storage**
- **Google Sheets** (production) or **In-memory** (demo)
- **Automatic ID generation** with timestamps
- **Real-time synchronization**

### **4. Matching Algorithm**
1. **Fetch all donors and NGOs**
2. **Convert locations to coordinates**
3. **Calculate distances** between each donor and NGO
4. **Find closest NGO** for each donor
5. **Return matched pairs** with distance information

## 🔗 Frontend Integration

The frontend (`script.js`) has been updated to:

- **Use REST API** instead of Firebase
- **Handle loading states** during form submission
- **Show success/error messages**
- **Reset forms** after successful submission
- **Include debugging functions** for viewing matches

## 🛠️ Development

### **Running in Development Mode**
```bash
# Demo mode (in-memory storage)
python app_sheets_demo.py

# Full mode (Google Sheets)
python app_sheets.py
```

### **Testing the API**
```bash
# Using curl
curl http://localhost:5000/api/health

# Using PowerShell
Invoke-RestMethod -Uri "http://localhost:5000/api/health"

# Using browser
http://localhost:5000/api/health
```

### **Debugging**
- **Check console logs** for API responses
- **Use `viewMatches()`** function in browser console
- **Monitor Flask debug output** for backend errors

## 📈 Benefits

### **For Users**
- **Simple interface** - Easy to use forms
- **Real-time matching** - Instant NGO connections
- **Location-based** - Find nearby organizations
- **Mobile-friendly** - Works on all devices

### **For Developers**
- **No database setup** - Google Sheets handles storage
- **Easy deployment** - Simple Flask app
- **Scalable** - Can handle multiple users
- **Extensible** - Easy to add new features

### **For Organizations**
- **Cost-effective** - Free Google Sheets storage
- **Collaborative** - Multiple people can view data
- **Exportable** - Easy to get data in various formats
- **Backup included** - Automatic Google Drive backup

## 🚀 Deployment Options

### **Local Development**
```bash
python app_sheets_demo.py
```

### **Production with Google Sheets**
1. Set up Google Cloud credentials
2. Deploy Flask app to your preferred hosting
3. Update frontend API URL
4. Configure environment variables

### **Cloud Platforms**
- **Heroku** - Easy Flask deployment
- **Google Cloud Run** - Serverless deployment
- **AWS Lambda** - Serverless functions
- **DigitalOcean** - VPS deployment

## 🔍 Troubleshooting

### **Common Issues**

1. **"Method Not Allowed"**
   - Check if the correct HTTP method is being used
   - Verify the endpoint URL is correct

2. **"Network Error"**
   - Ensure the Flask server is running
   - Check if the port 5000 is available
   - Verify CORS settings if needed

3. **"Geocoding Error"**
   - Check if the location string is valid
   - Ensure internet connection for geocoding service

4. **"Google Sheets Error"**
   - Verify credentials are set up correctly
   - Check if Google Sheets API is enabled
   - Ensure service account has proper permissions

### **Debug Commands**
```bash
# Check if server is running
netstat -ano | findstr :5000

# Kill all Python processes
taskkill /F /IM python.exe

# Test API endpoints
curl http://localhost:5000/api/health
```

## 🎉 Success!

Your XylemCSCIS Food Donation Platform is now running with:

- ✅ **Flask Backend API** with location-based matching
- ✅ **Google Sheets Integration** for data storage
- ✅ **Modern Frontend** with role-based forms
- ✅ **Smart Matching Algorithm** using geopy
- ✅ **Real-time Data Processing** and validation

The platform is ready to connect donors with NGOs and help reduce food waste while supporting communities in need!

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the `GOOGLE_SHEETS_SETUP.md` for detailed setup
3. Test with the demo version first
4. Check Flask debug output for backend errors
