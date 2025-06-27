from typing import Dict, Any, Optional
from config import Config
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class UserSettings(Base):
    __tablename__ = 'user_settings'
    
    user_id = Column(Integer, primary_key=True)
    settings = Column(JSON, default={})
    temp_data = Column(JSON, default={})

class Database:
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    async def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Get user settings"""
        session = self.Session()
        try:
            user = session.query(UserSettings).filter_by(user_id=user_id).first()
            if user:
                return user.settings
            return {}
        finally:
            session.close()
    
    async def update_user_settings(self, user_id: int, settings: Dict[str, Any]):
        """Update user settings"""
        session = self.Session()
        try:
            user = session.query(UserSettings).filter_by(user_id=user_id).first()
            if user:
                user.settings = {**user.settings, **settings}
            else:
                user = UserSettings(user_id=user_id, settings=settings)
                session.add(user)
            session.commit()
        finally:
            session.close()
    
    async def set_temp_data(self, user_id: int, key: str, value: Dict[str, Any]):
        """Set temporary data for user"""
        session = self.Session()
        try:
            user = session.query(UserSettings).filter_by(user_id=user_id).first()
            if user:
                if not user.temp_data:
                    user.temp_data = {}
                user.temp_data[key] = value
            else:
                user = UserSettings(user_id=user_id, temp_data={key: value})
                session.add(user)
            session.commit()
        finally:
            session.close()
    
    async def get_temp_data(self, user_id: int, key: str) -> Optional[Dict[str, Any]]:
        """Get temporary data for user"""
        session = self.Session()
        try:
            user = session.query(UserSettings).filter_by(user_id=user_id).first()
            if user and user.temp_data and key in user.temp_data:
                return user.temp_data[key]
            return None
        finally:
            session.close()
    
    async def delete_temp_data(self, user_id: int, key: str):
        """Delete temporary data for user"""
        session = self.Session()
        try:
            user = session.query(UserSettings).filter_by(user_id=user_id).first()
            if user and user.temp_data and key in user.temp_data:
                del user.temp_data[key]
                session.commit()
        finally:
            session.close()
    
    async def is_premium_user(self, user_id: int) -> bool:
        """Check if user is premium"""
        # In a real implementation, you'd check your payment system
        return False
