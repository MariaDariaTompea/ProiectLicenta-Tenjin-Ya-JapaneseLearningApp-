"""
Exercise system models.

Structure:
  Chapter  (capitol)    — e.g. "Hiragana Basics", "Greetings N5"
    └── Exercise (exercițiu) — e.g. "Write あ", "Translate 'hello'"
          └── Test  (test)   — individual question/answer inside an exercise
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.database import Base


class Chapter(Base):
    """A chapter / capitol — top-level grouping of exercises."""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)                       # e.g. "Hiragana — Vocale"
    description = Column(Text, default="")                       # short description
    category = Column(String, default="general")                 # grammar, vocabulary, culture, hiragana, katakana …
    level = Column(String, default="N5")                         # JLPT level
    order_index = Column(Integer, default=0)                     # display order
    image_url = Column(String, default="")                       # optional chapter icon/banner

    exercises = relationship("Exercise", back_populates="chapter", order_by="Exercise.order_index")


class Exercise(Base):
    """An exercise inside a chapter — groups several tests together."""
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    title = Column(String, nullable=False)                       # e.g. "Scrie caracterul あ"
    description = Column(Text, default="")
    exercise_type = Column(String, default="quiz")               # quiz, writing, listening, matching …
    order_index = Column(Integer, default=0)                     # display order inside chapter
    points = Column(Integer, default=10)                         # XP / points awarded

    chapter = relationship("Chapter", back_populates="exercises")
    tests = relationship("Test", back_populates="exercise", order_by="Test.order_index")


class Test(Base):
    """A single test / question inside an exercise."""
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    question = Column(Text, nullable=False)                      # the question text or prompt
    correct_answer = Column(String, nullable=False)              # expected correct answer
    option_a = Column(String, default="")                        # multiple-choice option A
    option_b = Column(String, default="")                        # multiple-choice option B
    option_c = Column(String, default="")                        # multiple-choice option C
    option_d = Column(String, default="")                        # multiple-choice option D
    test_type = Column(String, default="multiple_choice")        # multiple_choice, text_input, matching, drag_drop …
    image_url = Column(String, default="")                       # optional image for the question
    audio_url = Column(String, default="")                       # optional audio clip
    order_index = Column(Integer, default=0)                     # display order inside exercise
    explanation = Column(Text, default="")                       # shown after answering

    exercise = relationship("Exercise", back_populates="tests")
