from sqlalchemy.orm import Session
from models import User
from face_verify import verify_face


# =====================================
# Register New User
# =====================================

def create_user(
    db: Session,
    username: str,
    email: str,
    face_path: str,
    gesture_pattern: list
):

    user = User(
        username=username,
        email=email,
        face_path=face_path,
        gesture_pattern=gesture_pattern
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =====================================
# Get User by Username
# =====================================

def get_user_by_username(db: Session, username: str):

    return db.query(User).filter(
        User.username == username
    ).first()


# =====================================
# Get User by Email
# =====================================

def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


# =====================================
# Verify Gesture Pattern
# =====================================

def verify_gesture_pattern(user, input_pattern: list):

    if user is None:
        return False

    return user.gesture_pattern == input_pattern


# =====================================
# Login Authentication
# =====================================

# =====================================
# Login Authentication
# =====================================

def authenticate_user(
    db: Session,
    username: str,
    input_pattern: list
):

    print("\n========== LOGIN DEBUG ==========")

    user = get_user_by_username(db, username)

    if user is None:
        print("❌ User not found in database.")
        return None

    print("Username        :", username)
    print("Stored Pattern  :", user.gesture_pattern)
    print("Input Pattern   :", input_pattern)

    # Face Verification
    # TEMPORARY: Skip face verification
    face_verified = True
    print("Face Verified   : True (Temporary)")

    # Gesture Verification
    gesture_verified = verify_gesture_pattern(
        user,
        input_pattern
    )
    print("Gesture Verified:", gesture_verified)

    if face_verified and gesture_verified:
        print("✅ LOGIN SUCCESS")
        return user

    print("❌ LOGIN FAILED")
    return None

# =====================================
# Continuous Authentication
# =====================================

def continuous_authenticate(
    db: Session,
    username: str
):

    user = get_user_by_username(db, username)

    if user is None:
        return {
            "status": "locked",
            "message": "User not found."
        }

    # Verify current face
    face_verified = verify_face(username)

    if face_verified:
        return {
            "status": "verified",
            "message": "User verified successfully."
        }

    return {
        "status": "gesture_required",
        "message": "Face mismatch detected. Gesture verification required."
    }


# =====================================
# Continuous Gesture Verification
# =====================================

def verify_continuous_gesture(
    db: Session,
    username: str,
    input_pattern: list
):

    user = get_user_by_username(db, username)

    if user is None:
        return {
            "status": "locked",
            "message": "User not found."
        }

    if verify_gesture_pattern(user, input_pattern):
        return {
            "status": "verified",
            "message": "Gesture verified successfully."
        }

    return {
        "status": "locked",
        "message": "Gesture verification failed. Session locked."
    }


print("======================================")
print(" AirCanvas Secure Authentication Ready ")
print("======================================")