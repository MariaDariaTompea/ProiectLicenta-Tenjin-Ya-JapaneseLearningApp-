"""User and UserItem models"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    nickname = Column(String, default="")
    avatar_url = Column(String, default="/customisableprofile/defaultsettings/profileicondefault.png")
    banner_url = Column(String, default="/customisableprofile/defaultsettings/bannerdefault.png")
    current_level = Column(String, default="N5")
    # Progress tracking
    status_chapter  = Column(Integer, default=1, nullable=False, server_default="1")
    status_exercise = Column(Integer, default=1, nullable=False, server_default="1")
    # Equipped achievement slots (store achievement IDs)
    equipped_achievement_1 = Column(Integer, ForeignKey("achievements.id"), nullable=True)
    equipped_achievement_2 = Column(Integer, ForeignKey("achievements.id"), nullable=True)
    equipped_achievement_3 = Column(Integer, ForeignKey("achievements.id"), nullable=True)


class StatusLearning(Base):
    """Tracks a user's learning progress separately across modules"""
    __tablename__ = "status_learning"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    status_chapter_overall = Column(Integer, default=1, nullable=False, server_default="1")
    
    status_chapter_grammar = Column(Integer, default=1, nullable=False, server_default="1")
    status_exercise_grammar = Column(Integer, default=1, nullable=False, server_default="1")
    
    status_chapter_vocabulary = Column(Integer, default=1, nullable=False, server_default="1")
    status_exercise_vocabulary = Column(Integer, default=1, nullable=False, server_default="1")


class UserItem(Base):
    """Items (achievements, banners, icons) owned by a user"""
    __tablename__ = "user_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_type = Column(String, nullable=False)          # "achievement", "banner", "avatar"
    acquired_at = Column(DateTime, default=datetime.utcnow)
