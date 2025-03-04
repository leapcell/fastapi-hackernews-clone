from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    inspect,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime

# Get database connection information from environment variables
DATABASE_URL = os.getenv("DATABASE_DSN", "")

# Create a database engine
engine = create_engine(DATABASE_URL)
# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Define the Post model
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    link = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define a relationship with the Comment model
    comments = relationship("Comment", back_populates="post")


# Define the Comment model
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey("posts.id"))

    # Define a relationship with the Post model
    post = relationship("Post", back_populates="comments")


# Check and update database tables
def check_and_update_tables():
    inspector = inspect(engine)
    models = [Post, Comment]

    for model in models:
        table_name = model.__tablename__
        if not inspector.has_table(table_name):
            # Create the table if it doesn't exist
            print(f"Table {table_name} does not exist. Creating...")
            model.__table__.create(bind=engine)


# Provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
