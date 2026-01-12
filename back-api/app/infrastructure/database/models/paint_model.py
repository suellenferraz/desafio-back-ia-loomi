from sqlalchemy import Column, Integer, String, ARRAY, DateTime, CheckConstraint
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.infrastructure.database.connection import Base

class PaintModel(Base):
    """Model SQLAlchemy para Paint"""
    
    __tablename__ = "paints"
    __table_args__ = (
        CheckConstraint("environment IN ('interno', 'externo')", name="check_environment"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    color = Column(String(50), nullable=False)
    surface_type = Column(String(100), nullable=False)
    environment = Column(String(10), nullable=False)
    finish_type = Column(String(50), nullable=False)
    features = Column(ARRAY(String), nullable=False, default=list)
    line = Column(String(50), nullable=False, index=True)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<PaintModel(id={self.id}, name='{self.name}', line='{self.line}')>"