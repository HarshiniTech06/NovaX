// ===============================
// AirCanvas Secure Register Page
// ===============================

console.log("page1.js Loaded");

const API_URL = "http://127.0.0.1:8000";

let faceRegistered = false;
let gestureRegistered = false;
let gesturePattern = [];

// Elements
const faceBtn = document.getElementById("faceBtn");
const gestureBtn = document.getElementById("gestureBtn");
const registerForm = document.getElementById("registerForm");

// Disable gesture button initially
gestureBtn.disabled = true;

faceBtn.addEventListener("click", async () => {
    console.log("FACE BUTTON CLICKED");

    const username = document.getElementById("username").value.trim();

    if (!username) {
        alert("Please enter username");
        return;
    }

    faceBtn.disabled = true;
    faceBtn.innerHTML = "📷 Registering Face...";

    try {

        console.log("Sending request...");

        const response = await fetch(`${API_URL}/register-face`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username
            })
        });

        console.log("Response received");
        console.log("Status:", response.status);

        const data = await response.json();

        console.log("Response JSON:", data);

        faceRegistered = true;

        console.log("faceRegistered =", faceRegistered);

        faceBtn.innerHTML = "✅ Face Registered";
        gestureBtn.disabled = false;

        alert("Face Registered Successfully");

    } catch (err) {

        console.log(err);

    }

});

// ======================================
// Gesture Registration
// ======================================

gestureBtn.addEventListener("click", async () => {
    const username = document.getElementById("username").value.trim();

    if (!username) {
        alert("Please enter Username.");
        return;
    }

    gestureBtn.disabled = true;
    gestureBtn.innerHTML = "✋ Opening Camera...";

    try {
        const response = await fetch(`${API_URL}/register-gesture`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username
            })
        });

        let data = {};
        try {
            data = await response.json();
        } catch {
            data = {};
        }

        if (!response.ok) {
            throw new Error(
                data.detail ||
                data.message ||
                `Server Error (${response.status})`
            );
        }

        gesturePattern = data.pattern || [];
        gestureRegistered = true;

        gestureBtn.innerHTML = "✅ Gesture Registered";
        gestureBtn.disabled = true;

        alert("✅ Gesture Registered Successfully!\n\nNow click Create Account.");

    } catch (error) {
        console.error("Gesture Registration Error:", error);
        alert(error.message);

        gestureBtn.disabled = false;
        gestureBtn.innerHTML = "✋ Register Air Gesture";
    }
});

// ======================================
// Final Registration
// ======================================

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!username || !email) {
        alert("Please enter Username and Email.");
        return;
    }

    if (!faceRegistered) {
        alert("Please register your face first.");
        return;
    }

    if (!gestureRegistered) {
        alert("Please register your gesture first.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                face_path: `face_data/${username}.jpg`,
                gesture_pattern: gesturePattern
            })
        });

        let data = {};
        try {
            data = await response.json();
        } catch (e) {
            data = {};
        }

        if (!response.ok) {
            throw new Error(
                data.detail ||
                data.message ||
                `Server Error (${response.status})`
            );
        }

        alert("🎉 Account Created Successfully!");
        window.location.href = "../page2/page2.html";

    } catch (error) {
        console.error("Registration Error:", error);
        alert(error.message);
    }
});