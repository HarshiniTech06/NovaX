// ==========================================
// AirCanvas Secure Login Page
// ==========================================

console.log("Login Page Loaded");

const API_URL = "http://127.0.0.1:8000";

let faceVerified = false;
let gestureVerified = false;
let gesturePattern = [];

const faceBtn = document.getElementById("faceLoginBtn");
const gestureBtn = document.getElementById("gestureBtn");
const loginForm = document.getElementById("loginForm");

gestureBtn.disabled = true;

// ==========================================
// Face Verification
// ==========================================

faceBtn.addEventListener("click", async () => {
    console.log("✅ Face button clicked");

    const username = document.getElementById("username").value.trim();

    if (!username) {
        alert("Please enter a Username before verifying your face.");
        return;
    }

    console.log("1. Sending face verification request...");

    // UI Feedback: Disable button during processing
    faceBtn.disabled = true;
    faceBtn.innerHTML = "📷 Verifying Face...";

    try {
        const response = await fetch(`${API_URL}/verify-face`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username: username })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Face Verification Failed");
        }

        faceVerified = true;
        faceBtn.innerHTML = "✅ Face Verified";
        
        // Unlock next step
        gestureBtn.disabled = false;

        alert("Face Verified Successfully!");

    } catch (error) {
        console.error(error);
        alert(error.message);

        // Reset button state on failure
        faceBtn.disabled = false;
        faceBtn.innerHTML = "📷 Verify Face";
    }
});


// ==========================================
// Gesture Verification
// ==========================================

gestureBtn.addEventListener("click", async () => {
    const username = document.getElementById("username").value.trim();

    if (!username) {
        alert("Please enter Username");
        return;
    }

    gestureBtn.disabled = true;
    gestureBtn.innerHTML = "✋ Verifying Gesture...";

    try {
        const response = await fetch(`${API_URL}/verify-gesture`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Gesture Verification Failed");
        }

        gestureVerified = true;
        gesturePattern = data.pattern || [];
        gestureBtn.innerHTML = "✅ Gesture Verified";

        alert("Gesture Verified Successfully!");

    } catch (error) {
        console.error(error);
        alert(error.message);

        gestureBtn.disabled = false;
        gestureBtn.innerHTML = "✋ Verify Gesture";
    }
});


// ==========================================
// Login
// ==========================================

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();

    if (!username) {
        alert("Please enter Username");
        return;
    }

    if (!faceVerified) {
        alert("Please verify your Face first.");
        return;
    }

    if (!gestureVerified) {
        alert("Please verify your Gesture first.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                pattern: gesturePattern
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Login Failed");
        }

        alert("🎉 Login Successful!");
        window.location.href = "../dashboard/dashboard.html";

    } catch (error) {
        console.error(error);
        alert(error.message);
    }
});