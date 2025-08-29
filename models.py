from sqlalchemy import Column, String, Integer, Text, Index
from db import Base


class History(Base):
    __tablename__ = 'history'

    id = Column(String, primary_key=True)  # UUID
    text = Column(Text, nullable=False)
    lang = Column(String(8), nullable=True)
    file = Column(String, nullable=False)
    created_at = Column(Integer, index=True, nullable=False)


Index('idx_history_created_at', History.created_at)
