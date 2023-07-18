from enum import unique
import imp
from msilib.schema import Upgrade
import string
from turtle import update
from unicodedata import numeric
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Float, VARCHAR, Numeric
from traitlets import default
from database.base import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime



class Specification(Base):
    __tablename__ = 'specifications'

    id = Column(Integer, primary_key=True, index=True)
    coding = Column(String)         # Кодування
    name = Column(String)           # Найменування
    number = Column(String)         # Кількість
Base.metadata.create_all(bind=engine)


class Cost(Base):
    __tablename__ = 'costs'

    id = Column(Integer, primary_key=True, index=True)
    coding = Column(String)         # Кодування
    name = Column(String)           # Найменування
    number = Column(Integer)        # Кількість деталей
    marka = Column(String)          # Марка матеріалу
    profile = Column(String)        # Профіль    
    rate_costs = Column(Float)      # Норми витрат (кг.) на 1шт.
    rates_costs = Column(Float)     # Норми витрат (кг.) 
    norm_years = Column(Float)      # Норми годин на 1 деталь
    cost_materials = Column(Float)  # Собівартість матеріалу
    norms_years = Column(Float)     # Нормо годин
    norms_sec = Column(Float)       #Норма в секундах
    price_kg = Column(Float)        # Ціна за кг.
Base.metadata.create_all(bind=engine)

