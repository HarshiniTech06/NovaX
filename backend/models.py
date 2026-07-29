from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone

from database import Base


# -----------------------------
# User Table Model
# -----------------------------
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    face_path = Column(
        String,
        nullable=False
    )

    # Store gesture pattern directly
    # Example: [1, 2, 5, 8, 9]
    gesture_pattern = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


print("✅ Models Loaded Successfully!")