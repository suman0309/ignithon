// Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Initialize Firestore
const db = firebase.firestore();

// Form elements
const donorForm = document.getElementById('donorForm');
const ngoForm = document.getElementById('ngoForm');
const successMessage = document.getElementById('successMessage');
const successText = document.getElementById('successText');

// Donor form submission
donorForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(donorForm);
    const donorData = {
        foodType: formData.get('foodType'),
        quantity: formData.get('quantity'),
        expiryTime: parseInt(formData.get('expiryTime')),
        location: formData.get('location'),
        timestamp: firebase.firestore.FieldValue.serverTimestamp(),
        type: 'donor'
    };
    
    try {
        await db.collection('donations').add(donorData);
        showSuccessMessage('Donation submitted successfully! Your food donation has been recorded.');
        donorForm.reset();
    } catch (error) {
        console.error('Error submitting donation:', error);
        showSuccessMessage('Error submitting donation. Please try again.');
    }
});

// NGO form submission
ngoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(ngoForm);
    const ngoData = {
        ngoName: formData.get('ngoName'),
        foodNeeded: formData.get('foodNeeded'),
        location: formData.get('location'),
        timestamp: firebase.firestore.FieldValue.serverTimestamp(),
        type: 'ngo'
    };
    
    try {
        await db.collection('ngoRequests').add(ngoData);
        showSuccessMessage('NGO request submitted successfully! Your food request has been recorded.');
        ngoForm.reset();
    } catch (error) {
        console.error('Error submitting NGO request:', error);
        showSuccessMessage('Error submitting NGO request. Please try again.');
    }
});

// Show success message
function showSuccessMessage(message) {
    successText.textContent = message;
    successMessage.classList.remove('hidden');
}

// Hide success message
function hideSuccessMessage() {
    successMessage.classList.add('hidden');
}

// Close success message when clicking outside
successMessage.addEventListener('click', (e) => {
    if (e.target === successMessage) {
        hideSuccessMessage();
    }
});

// Close success message with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !successMessage.classList.contains('hidden')) {
        hideSuccessMessage();
    }
});

// Form validation and enhancement
function enhanceFormValidation() {
    const inputs = document.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (input.value.trim() === '') {
                input.style.borderColor = '#dc3545';
            } else {
                input.style.borderColor = '#e1e5e9';
            }
        });
        
        input.addEventListener('input', () => {
            if (input.value.trim() !== '') {
                input.style.borderColor = '#e1e5e9';
            }
        });
    });
}

// Initialize form validation
document.addEventListener('DOMContentLoaded', () => {
    enhanceFormValidation();
    
    // Add loading state to buttons
    const submitButtons = document.querySelectorAll('.submit-btn');
    
    submitButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.textContent = 'Submitting...';
            button.disabled = true;
            
            // Reset button after form submission
            setTimeout(() => {
                button.textContent = button.textContent.includes('Donation') ? 'Submit Donation' : 'Submit Request';
                button.disabled = false;
            }, 2000);
        });
    });
});

// Optional: Add some helpful console messages for setup
console.log('Food Donation Platform loaded successfully!');
console.log('Remember to replace the Firebase configuration with your own credentials.');
console.log('You can get your Firebase config from: https://console.firebase.google.com/');
