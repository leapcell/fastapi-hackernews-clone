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
from sqlalchemy.exc import OperationalError
import os
from datetime import datetime

# Get the database connection string from environment variables, default to empty string
DATABASE_URL = os.getenv("DATABASE_DSN", "")


def get_engine():
    """
    Get the database engine and session factory.
    Attempt to connect to the database and return the engine and session factory if successful.
    """
    try:
        # Create a database engine
        engine = create_engine(DATABASE_URL)
        # Create a session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Test the database connection
        with engine.connect() as connection:
            print("Connection to PostgreSQL successful!")
            return engine, SessionLocal
    except OperationalError as e:
        print(
            f"Failed to connect to PostgreSQL, DATABASE_URL {DATABASE_URL}, error: {e}"
        )
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}, DATABASE_URL {DATABASE_URL}")
        return None, None
    return None, None


# Create a base class for declarative models
Base = declarative_base()


# Define the Post model
class Post(Base):
    __tablename__ = "posts"
    # Primary key and indexed column
    id = Column(Integer, primary_key=True, index=True)
    # Indexed title column
    title = Column(String, index=True)
    # Link column
    link = Column(String)
    # Content column
    content = Column(Text)
    # Creation time column, default to current UTC time
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define a one-to-many relationship with the Comment model
    comments = relationship("Comment", back_populates="post")


# Define the Comment model
class Comment(Base):
    __tablename__ = "comments"
    # Primary key and indexed column
    id = Column(Integer, primary_key=True, index=True)
    # Content column
    content = Column(Text)
    # Creation time column, default to current UTC time
    created_at = Column(DateTime, default=datetime.utcnow)
    # Foreign key referencing the Post model
    post_id = Column(Integer, ForeignKey("posts.id"))

    # Define a many-to-one relationship with the Post model
    post = relationship("Post", back_populates="comments")


# Check and update database tables
def check_and_update_tables():
    """
    Check if the necessary database tables exist, and create them if not.
    """
    engine, SessionLocal = get_engine()
    if not engine:
        return

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
    """
    Get a database session.
    Return a session if the database connection is successful, otherwise return None.
    """
    engine, SessionLocal = get_engine()
    if not engine:
        return None
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
