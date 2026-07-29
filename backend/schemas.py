from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List


# --------------------------------
# Register User Schema
# --------------------------------
class UserRegister(BaseModel):

    username: str

    email: EmailStr

    face_path: str

    gesture_pattern: List[int]


# --------------------------------
# Login User Schema
# --------------------------------
class UserLogin(BaseModel):

    username: str

    pattern: List[int]


# --------------------------------
# Continuous Authentication Request
# --------------------------------
class ContinuousAuthRequest(BaseModel):

    username: str


# --------------------------------
# Gesture Verification Request
# --------------------------------
class GestureVerifyRequest(BaseModel):

    username: str

    pattern: List[int]


# --------------------------------
# Continuous Authentication Response
# --------------------------------
class ContinuousAuthResponse(BaseModel):

    status: str

    message: str


# --------------------------------
# User Response
# --------------------------------
class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    face_path: str

    gesture_pattern: List[int]

    model_config = ConfigDict(from_attributes=True)