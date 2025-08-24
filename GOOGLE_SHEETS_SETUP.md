# Google Sheets Database Setup Guide

This guide will help you set up Google Sheets as the database for the XylemCSCIS Food Donation Platform.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** or select an existing one
3. **Enable Google Sheets API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 3. Create Service Account

1. **Go to "APIs & Services" → "Credentials"**
2. **Click "Create Credentials" → "Service Account"**
3. **Fill in the details**:
   - Service account name: `xylemcscis-food-donation`
   - Description: `Service account for food donation platform`
4. **Click "Create and Continue"**
5. **Skip role assignment** (click "Continue")
6. **Click "Done"**

### 4. Generate Service Account Key

1. **Click on your service account** in the credentials list
2. **Go to "Keys" tab**
3. **Click "Add Key" → "Create new key"**
4. **Choose "JSON" format**
5. **Click "Create"** - this will download a JSON file
6. **Rename the file** to `google-sheets-credentials.json`
7. **Place it in your project root** (same folder as `app_sheets.py`)

### 5. Share Google Sheets

The service account will automatically create two Google Sheets:
- **"Donors"** - for donor data
- **"NGOs"** - for NGO data

**To view the sheets:**
1. Go to [Google Drive](https://drive.google.com)
2. Look for the sheets with names "Donors" and "NGOs"
3. **Share them** with your email address for viewing/editing

## 🔧 Configuration Options

### Option A: Service Account Key File (Recommended for Development)

1. **Place the JSON file** in your project root
2. **Name it** `google-sheets-credentials.json`
3. **Run the app**:
   ```bash
   python app_sheets.py
   ```

### Option B: Environment Variables (Recommended for Production)

Set these environment variables:

```bash
export GOOGLE_PROJECT_ID="your-project-id"
export GOOGLE_PRIVATE_KEY_ID="your-private-key-id"
export GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
export GOOGLE_CLIENT_EMAIL="your-service-account@your-project.iam.gserviceaccount.com"
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

## 📊 Google Sheets Structure

### Donors Sheet
| ID | Food Type | Quantity | Expiry Time (hours) | Location | Timestamp |
|----|-----------|----------|-------------------|----------|-----------|
| donor_20231201_103000 | Rice | 10 kg | 48 | New York, NY | 2023-12-01T10:30:00Z |

### NGOs Sheet
| ID | NGO Name | Food Needed | Location | Timestamp |
|----|----------|-------------|----------|-----------|
| ngo_20231201_083000 | Food Bank NYC | Rice, Bread, Vegetables | Manhattan, NY | 2023-12-01T08:30:00Z |

## 🚀 Running the Application

```bash
python app_sheets.py
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### GET Endpoints
- **`GET /api/matches`** - Get donor-NGO matches
- **`GET /api/donors`** - Get all donors
- **`GET /api/ngos`** - Get all NGOs
- **`GET /api/health`** - Health check

### POST Endpoints
- **`POST /api/donors`** - Add new donor
- **`POST /api/ngos`** - Add new NGO

## 📝 Example API Usage

### Add a Donor
```bash
curl -X POST http://localhost:5000/api/donors \
  -H "Content-Type: application/json" \
  -d '{
    "foodType": "Rice",
    "quantity": "10 kg",
    "expiryTime": 48,
    "location": "New York, NY"
  }'
```

### Add an NGO
```bash
curl -X POST http://localhost:5000/api/ngos \
  -H "Content-Type: application/json" \
  -d '{
    "ngoName": "Food Bank NYC",
    "foodNeeded": "Rice, Bread, Vegetables",
    "location": "Manhattan, NY"
  }'
```

### Get Matches
```bash
curl http://localhost:5000/api/matches
```

## 🔗 Frontend Integration

Update your frontend JavaScript to use the new API endpoints:

```javascript
// Add donor
async function addDonor(donorData) {
    const response = await fetch('http://localhost:5000/api/donors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(donorData)
    });
    return response.json();
}

// Add NGO
async function addNGO(ngoData) {
    const response = await fetch('http://localhost:5000/api/ngos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(ngoData)
    });
    return response.json();
}

// Get matches
async function getMatches() {
    const response = await fetch('http://localhost:5000/api/matches');
    return response.json();
}
```

## 🛡️ Security Considerations

1. **Keep credentials secure** - Don't commit the JSON file to version control
2. **Use environment variables** in production
3. **Limit API access** - Only enable necessary Google APIs
4. **Monitor usage** - Check Google Cloud Console for API usage

## 🔍 Troubleshooting

### Common Issues

1. **"Service account not found"**
   - Verify the JSON file is in the correct location
   - Check that the service account exists in Google Cloud Console

2. **"API not enabled"**
   - Enable Google Sheets API in Google Cloud Console
   - Wait a few minutes for changes to propagate

3. **"Permission denied"**
   - Ensure the service account has the necessary permissions
   - Check that the Google Sheets are shared with the service account email

4. **"Sheet not found"**
   - The app will automatically create sheets if they don't exist
   - Check Google Drive for the created sheets

### Debug Mode

Run with debug mode for detailed error messages:

```bash
export FLASK_ENV=development
python app_sheets.py
```

## 📈 Benefits of Google Sheets

1. **Easy to view data** - No database setup required
2. **Real-time collaboration** - Multiple people can view/edit
3. **Export capabilities** - Easy to export to CSV/Excel
4. **No hosting costs** - Google Sheets is free
5. **Backup included** - Automatic Google Drive backup

## 🎯 Next Steps

1. **Test the API** with sample data
2. **Integrate with frontend** forms
3. **Set up monitoring** for API usage
4. **Configure production** environment variables
5. **Set up automated backups** if needed

## 📞 Support

If you encounter issues:
1. Check the Google Cloud Console for API errors
2. Verify your service account permissions
3. Ensure all environment variables are set correctly
4. Check the Flask debug output for detailed error messages
