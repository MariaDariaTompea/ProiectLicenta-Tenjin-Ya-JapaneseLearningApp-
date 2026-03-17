"""Achievement model"""

from sqlalchemy import Column, Integer, String
from core.database import Base


class Achievement(Base):
    """All possible achievements / collectible items in the game"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False, default="/customisableprofile/defaultsettings/defaultgem.png")
    category = Column(String, default="general")  # general, hiragana, katakana, etc.
