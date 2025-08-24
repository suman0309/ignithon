<<<<<<< HEAD
# Food Donation Platform

A simple web application that connects food donors with NGOs to reduce food waste. Built with HTML, CSS, JavaScript, and Firebase Firestore.

## Features

- **Donor Form**: Allows individuals to submit food donations with details like food type, quantity, expiry time, and location
- **NGO Form**: Enables NGOs to request specific food items with their location
- **Firebase Integration**: Stores all form data in Firestore database
- **Mobile-Friendly**: Responsive design that works on all devices
- **Success Messages**: User-friendly feedback after form submission

## Setup Instructions

### 1. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Firestore Database:
   - Go to Firestore Database in the sidebar
   - Click "Create Database"
   - Choose "Start in test mode" for development
4. Get your Firebase configuration:
   - Go to Project Settings (gear icon)
   - Scroll down to "Your apps" section
   - Click "Add app" and select Web
   - Copy the configuration object

### 2. Update Firebase Configuration

Open `script.js` and replace the `firebaseConfig` object with your actual Firebase configuration:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project-id.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project-id.appspot.com",
    messagingSenderId: "your-sender-id",
    appId: "your-app-id"
};
```

### 3. Firestore Security Rules

For development, you can use test mode. For production, update your Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true; // For development only
    }
  }
}
```

### 4. Run the Application

1. Open `index.html` in a web browser
2. Or serve the files using a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js (if you have http-server installed)
   npx http-server
   ```

## File Structure

```
├── index.html          # Main HTML file with forms
├── styles.css          # CSS styling and responsive design
├── script.js           # JavaScript with Firebase integration
└── README.md           # This file
```

## Form Fields

### Donor Form
- **Food Type**: Type of food being donated
- **Quantity**: Amount of food (e.g., "5 kg", "10 packets")
- **Expiry Time**: Hours until food expires
- **Location**: Donor's location

### NGO Form
- **NGO Name**: Name of the organization
- **Food Needed**: Type of food required
- **Location**: NGO's location

## Database Collections

The application creates two collections in Firestore:

1. **`donations`**: Stores donor form submissions
2. **`ngoRequests`**: Stores NGO form submissions

Each document includes:
- Form data
- Timestamp
- Type identifier

## Features

- ✅ Responsive design for mobile and desktop
- ✅ Form validation
- ✅ Success messages
- ✅ Loading states
- ✅ Firebase Firestore integration
- ✅ Clean and modern UI
- ✅ Keyboard navigation support

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

1. **Firebase not connecting**: Check your configuration in `script.js`
2. **Forms not submitting**: Ensure Firestore is enabled and rules allow write access
3. **Styling issues**: Make sure `styles.css` is in the same directory as `index.html`

## License

This project is open source and available under the MIT License.
=======
# ignithon
kit hackathon
>>>>>>> 2e9bed8c9fcafc34f7be79d8347dabe92c98a6a0
