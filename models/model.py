from sqlalchemy import Column
from sqlalchemy.types import Integer, String,Unicode, Date, Time, DateTime,Float
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric as Decimal,Boolean, NUMERIC
from passlib.context import CryptContext
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class EntityBank(Base):
    __tablename__ = "tbl_banks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class EntityBankBranch(Base):
    __tablename__ = "tbl_bank_branch"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    bank_id = Column(Unicode(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
