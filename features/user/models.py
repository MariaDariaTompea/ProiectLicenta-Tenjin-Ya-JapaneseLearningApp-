"""User, UserProfile, UserPhoto, UserItem, and StatusLearning models"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime


class User(Base):
    """Core user account — kept minimal"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    nickname = Column(String, default="")
    current_level = Column(String, default="N5")

    # Relationships
    profile = relationship("UserProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    photos = relationship("UserPhoto", back_populates="user", cascade="all, delete-orphan")
    items = relationship("UserItem", back_populates="user", cascade="all, delete-orphan")
    status = relationship("StatusLearning", uselist=False, back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    """Customisable profile data — avatar, banner, equipped achievements"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    avatar_url = Column(String, default="/customisableprofile/defaultsettings/profileicondefault.png")
    banner_url = Column(String, default="/customisableprofile/defaultsettings/bannerdefault.png")

    # Equipped achievement slots (store achievement IDs)
    equipped_achievement_1 = Column(Integer, ForeignKey("achievements.id"), nullable=True)
    equipped_achievement_2 = Column(Integer, ForeignKey("achievements.id"), nullable=True)
    equipped_achievement_3 = Column(Integer, ForeignKey("achievements.id"), nullable=True)

    user = relationship("User", back_populates="profile")


class UserPhoto(Base):
    """Photos uploaded by users (avatars, banners, gallery)"""
    __tablename__ = "user_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    photo_type = Column(String, nullable=False, default="avatar")  # "avatar", "banner", "gallery"
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="photos")


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

    user = relationship("User", back_populates="status")


class UserItem(Base):
    """Items (achievements, banners, icons) owned by a user"""
    __tablename__ = "user_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, nullable=False)
    item_type = Column(String, nullable=False)          # "achievement", "banner", "avatar"
    acquired_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="items")
