"""
Exercise system models.

Structure:
  Proficiency (JLPT level)  — e.g. N5, N4, N3, N2, N1
    └── Chapter  (capitol)    — e.g. "Hiragana Basics", "Greetings N5"
          └── Exercise (exercițiu) — e.g. "Hiragana & Katakana Course", "Vocabulary Quiz"
                └── Test  (test)   — individual question/answer inside an exercise
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Proficiency(Base):
    """A JLPT proficiency level — top-level grouping."""
    __tablename__ = "proficiencies"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, unique=True, nullable=False)          # "N5", "N4", "N3", "N2", "N1"
    name = Column(String, nullable=False, default="")            # e.g. "Beginner"
    description = Column(Text, default="")                       # short description
    order_index = Column(Integer, default=0)                     # display order (N5=1, N4=2 ...)

    chapters = relationship("Chapter", back_populates="proficiency", order_by="Chapter.order_index")


class Chapter(Base):
    """A chapter / capitol — groups exercises under a proficiency level."""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    proficiency_id = Column(Integer, ForeignKey("proficiencies.id"), nullable=False)
    title = Column(String, nullable=False)                       # e.g. "Hiragana — Vocale"
    description = Column(Text, default="")                       # short description
    category = Column(String, default="general")                 # grammar, vocabulary, culture
    order_index = Column(Integer, default=0)                     # display order
    image_url = Column(String, default="")                       # representative image
    pdf_url = Column(String, default="")                         # optional PDF content (mainly for culture)

    proficiency = relationship("Proficiency", back_populates="chapters")
    exercises = relationship("Exercise", back_populates="chapter", order_by="Exercise.order_index")


class Exercise(Base):
    """An exercise inside a chapter — groups several tests together."""
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    title = Column(String, nullable=False)                       # e.g. "Hiragana & Katakana Course"
    description = Column(Text, default="")
    theory_content = Column(Text, default="")                    # html/markdown theory shown before test
    exercise_type = Column(String, default="quiz")               # quiz, course, examination, interactive
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
    options = Column(Text, default="")                           # JSON string: ["opt1","opt2","opt3","opt4"]
    test_type = Column(String, default="multiple_choice")        # multiple_choice, text_input, matching, drag_drop
    image_url = Column(String, default="")                       # optional image for the question
    audio_url = Column(String, default="")                       # optional audio clip
    order_index = Column(Integer, default=0)                     # display order inside exercise
    explanation = Column(Text, default="")                       # shown after answering

    exercise = relationship("Exercise", back_populates="tests")
