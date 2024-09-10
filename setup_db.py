# db.py

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///feedback.db"   

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Feedback model
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, index=True)
    response = Column(Text)
    feedback = Column(String(10))

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
