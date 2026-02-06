from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Table
from sqlalchemy.orm import relationship
from app.database import Base

project_members = Table(
    'project_members',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship('User', foreign_keys=[owner_id])
    members = relationship('User', secondary=project_members, backref='projects')
