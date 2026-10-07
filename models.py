from sqlalchemy import Column, Integer, String, Float
from database import Base

class MovieDB(Base):
    __tablename__ = "movies"  # 告诉它对应数据库里的 movies 表

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    link = Column(String, nullable=True)
