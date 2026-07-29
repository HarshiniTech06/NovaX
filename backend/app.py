from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import traceback
from fastapi.middleware.cors import CORSMiddleware
from face import register_face
from gesture import register_gesture


from database import SessionLocal, Base, engine
from models import User
from schemas import (
    UserRegister,
    UserLogin,
    ContinuousAuthRequest,
    GestureVerifyRequest
)

from auth import (
    create_user,
    get_user_by_username,
    authenticate_user,
    continuous_authenticate,
    verify_continuous_gesture
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AirCanvas Secure API",
    version="2.0"

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to AirCanvas Secure API 🚀"
    }


# -----------------------------
# Register
# -----------------------------
# -----------------------------
# Register
# -----------------------------
@app.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        print("\n========== REGISTER REQUEST ==========")
        print("Username :", user.username)
        print("Email    :", user.email)
        print("Face     :", user.face_path)
        print("Gesture  :", user.gesture_pattern)

        # Check Username
        existing_user = get_user_by_username(db, user.username)
        print("Existing Username :", existing_user)

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists."
            )

        # Check Email
        from auth import get_user_by_email

        existing_email = get_user_by_email(db, user.email)
        print("Existing Email :", existing_email)

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

        # Create User
        new_user = create_user(
            db=db,
            username=user.username,
            email=user.email,
            face_path=user.face_path,
            gesture_pattern=user.gesture_pattern
        )

        print("✅ User Registered Successfully")

        return {
            "message": "User Registered Successfully!",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        print("\n========== REGISTER ERROR ==========")
        traceback.print_exc()
        print("====================================")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/register-face")
def register_face_api(data: dict):
    try:
        print("========== REGISTER FACE ==========")

        username = data["username"]
        print("Username:", username)

        print("Calling register_face()...")

        face_path = register_face(username)

        print("Returned from register_face()")
        print("Face Path:", face_path)

        return {
            "message": "Face Registered Successfully",
            "face_path": face_path
        }

    except Exception as e:
        print("ERROR:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register-gesture")
def register_gesture_api(data: dict):

    username = data["username"]

    pattern = register_gesture(username)

    return {
        "message": "Gesture Registered Successfully",
        "pattern": pattern
    }
@app.post("/login")
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    print(">>> LOGIN API HIT <<<")

    user = authenticate_user(
        db=db,
        username=credentials.username,
        input_pattern=credentials.pattern
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication Failed"
        )

    return {
        "message": "Login Successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }






# -----------------------------
# Continuous Authentication
# -----------------------------
@app.post("/continuous-auth")
def continuous_auth(
    request: ContinuousAuthRequest,
    db: Session = Depends(get_db)
):

    return continuous_authenticate(
        db,
        request.username
    )



# -----------------------------
# Get User
# -----------------------------
@app.get("/user/{username}")
def get_user(
    username: str,
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        username
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user