from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class SessionModel(Base):
    """Model SQLAlchemy para Session"""
    
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_user_expires', 'user_id', 'expires_at'),
    )
    
    def __repr__(self):
        return f"<SessionModel(id={self.id}, user_id={self.user_id}, session_id='{self.session_id[:8] if len(self.session_id) > 8 else self.session_id}...')>"
