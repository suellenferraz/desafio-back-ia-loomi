from sqlalchemy import Column, Integer, String, ARRAY, Boolean, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func
from app.infrastructure.database.connection import Base

class UserModel(Base):
    """Model SQLAlchemy para User"""
    
    __tablename__ = "users"
    
    __table_args__ = (
        CheckConstraint("array_length(roles, 1) > 0", name="check_roles_not_empty"),
        UniqueConstraint('username', name='uq_username'),
        UniqueConstraint('email', name='uq_email'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False) 
    roles = Column(ARRAY(String), nullable=False, default=[])
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, username='{self.username}', email='{self.email}', roles={self.roles})>"
