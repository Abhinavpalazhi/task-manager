from sqlalchemy import Column, Integer, String
from database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_email = Column(String, index=True, nullable=False)
