from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    
    polls = relationship("Poll", back_populates="owner")
    votes = relationship("UserOption", back_populates="user")
    posts = relationship("Post", back_populates="author")

class Poll(Base):
    __tablename__ = "polls"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="polls")
    options = relationship("Option", back_populates="poll", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="poll")

class Option(Base):
    __tablename__ = "options"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(100))
    poll_id = Column(Integer, ForeignKey("polls.id"))
    
    poll = relationship("Poll", back_populates="options")
    votes = relationship("UserOption", back_populates="option")

class UserOption(Base):
    __tablename__ = "user_options"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    option_id = Column(Integer, ForeignKey("options.id"), primary_key=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))  # Добавили poll_id
    
    user = relationship("User", back_populates="votes")
    option = relationship("Option", back_populates="votes")

