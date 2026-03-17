"""Hiragana and Katakana models"""

from sqlalchemy import Column, Integer, String
from core.database import Base


class Hiragana(Base):
    __tablename__ = "hiraganacharacters"

    id = Column(Integer, primary_key=True, index=True)
    character = Column(String)
    romaji = Column(String)
    image_filename = Column(String)


class Katakana(Base):
    __tablename__ = "katakanacharacters"

    id = Column(Integer, primary_key=True, index=True)
    character = Column(String)
    romaji = Column(String)
    image_filename = Column(String)
