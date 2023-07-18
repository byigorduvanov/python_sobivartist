from code import interact
from enum import unique
import imp
from msilib.schema import Upgrade
import string
from turtle import update
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Float, VARCHAR
from traitlets import default
from database.base import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, index=True)                      #
    marka = Column(String)                                                  # Марка матеріалу
    profile = Column(String)                                                # Профіль
    weight= Column(Float)                                                   # Вага п/м
    price= Column(Float)                                                    # Ціна за 1т.
    notes = Column(String)                                                  #
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
Base.metadata.create_all(bind=engine)



class Detail(Base):
    __tablename__ = 'details'

    id = Column(Integer, primary_key=True, index=True)                      #
    coding = Column(VARCHAR(13))                                            # Кодування
    name = Column(String)                                                   # Найменування
    product_type= Column(Integer)   
    material_id = Column(Integer, ForeignKey("materials.id"))               #
    lenght_workpiece = Column(Float)                                        # Довжина заготовки
    width_workpiece = Column(Float)                                         # Ширина заготовки
    trimming = Column(Float)                                                # Торцовка
    lenght_detail = Column(Float)                                           # Довжина деталі
    rate_costs = Column(Float)                                              # Норма розтрат, мм.
    notes = Column(String)
    price = Column(Float)                                                   # ціна
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
    Material = relationship("Material")
Base.metadata.create_all(bind=engine)


class Detail_change(Base):
    __tablename__ = 'detail_changes'

    id = Column(Integer, primary_key=True, index=True)
    detail_id = Column(Integer)                                             #
    coding = Column(VARCHAR(13))                                            # Кодування
    name = Column(String)                                                   # Найменування
    product_type= Column(Integer)   
    material_id = Column(Integer)               #
    lenght_workpiece = Column(Float)                                        # Довжина заготовки
    width_workpiece = Column(Float)                                         # Ширина заготовки
    trimming = Column(Float)                                                # Торцовка
    lenght_detail = Column(Float)                                           # Довжина деталі
    rate_costs = Column(Float)                                              # Норма розтрат, мм.
    notes = Column(String)
    price = Column(Float)                                                   # ціна
    date_created = Column(String)
    date_updated = Column(String)
Base.metadata.create_all(bind=engine)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    is_complete = Column(Boolean, default=False)
    notes = Column(String)
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
Base.metadata.create_all(bind=engine)


class Serie(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, index=True)                      
    name_serie = Column(String)                                             # Назва серії кранів
    notes = Column(String)                                                  # 
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
Base.metadata.create_all(bind=engine)


class Data(Base):
    __tablename__ = 'datas'

    id = Column(Integer, primary_key=True, index=True)
    name_data = Column(String)    
    notes = Column(String)
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
Base.metadata.create_all(bind=engine)


class Vavle(Base):
    __tablename__ = 'vavles'

    id = Column(Integer, primary_key=True, index=True)
    serie_id = Column(Integer, ForeignKey("series.id"))                     #
    detail_id = Column(Integer, ForeignKey("details.id"))                   #
    Serie = relationship("Serie")
    Detail = relationship("Detail")
    notes = Column(String)
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)
Base.metadata.create_all(bind=engine)

class Collective(Base):
    __tablename__ = 'colectives'

    id = Column(Integer, primary_key=True, index=True)
    collective_id = Column(Integer, ForeignKey("details.id"))               #
    collective_coding = Column(VARCHAR(13))                                 # Кодування
    sequence_number = Column(Integer)                                       # Порядковий номер
    detail_id = Column(Integer)                                             # Кодування деталі    
    number = Column(Float)                                                  # Кількість деталей в зборці
    notes = Column(String)                                                  # 
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)         
    Detail = relationship("Detail")
Base.metadata.create_all(bind=engine)


class Norm_year(Base):
    __tablename__ = 'norm_years'

    id = Column(Integer, primary_key=True, index=True)                      #
    detail_id = Column(Integer, ForeignKey("details.id"))                   #
    norm_year_coding = Column(VARCHAR(13))                                  # Кодування        
    norm_years = Column(Float)                                              # Нормо-годин
    notes = Column(String)                                                  # 
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.utcnow)         
    Detail = relationship("Detail")
Base.metadata.create_all(bind=engine)


class Material_coming(Base):
    __tablename__ = 'material_comings'

    id = Column(Integer, primary_key=True, index=True)                      #
    material_id = Column (Integer, ForeignKey("materials.id"))
    price= Column(Float)  
    availability = Column (Float)                                           # Кількість приходу
    notes = Column(String)                                                  # Номер документу (Накладна, партія)
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
    Material = relationship("Material")
Base.metadata.create_all(bind=engine)


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True, index=True)                      #
    name = Column(String)                                                   # Назва операції
    notes = Column(String)                                                  # примітки
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
Base.metadata.create_all(bind=engine)


class Operation_execution(Base):
    __tablename__ = 'operation_executions'

    id = Column(Integer, primary_key=True, index=True)                      #
    operation_id = Column(Integer, ForeignKey("operations.id"))             # id операція
    detail_id = Column(Integer)                                             # id деталь
    material_coming_id = Column(Integer)                                    # Матеріал з таблиці приходу матеріалу
    number = Column(Integer)                                                # Кількість деталей в операції
    unit = Column(String)                                                   # Підрозділ виконання
    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
    Operation = relationship("Operation")
Base.metadata.create_all(bind=engine)



class Od_vumir(Base):
    __tablename__ = 'od_vumirs'

    id = Column(Integer, primary_key=True, index=True)
    od_vumir = Column(String)       # Кодування
    name = Column(String)           # Найменування

Base.metadata.create_all(bind=engine)


class Perelik(Base):
    __tablename__ = 'pereliks'

    id = Column(Integer, primary_key=True, index=True)                      #
    coding = Column(VARCHAR(13))                                            # Кодування
    name = Column(String)                                                   # id деталь

    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
Base.metadata.create_all(bind=engine)


class Oblik(Base):
    __tablename__ = 'obliks'

    id = Column(Integer, primary_key=True, index=True)                      #
    perelik_id = Column(Integer, ForeignKey("pereliks.id"))
    operation = Column(Integer, ForeignKey("operations.id"))  
    number = Column(Integer)                                             # Кодування
    resurs = Column(Integer, ForeignKey("pereliks.id"))
    od_vumir = Column(Integer, ForeignKey("od_vumirs.id"))      
    kst = Column(String)  

    Operation = relationship("Operation")
    Od_vumir = relationship("Od_vumir")


    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
Base.metadata.create_all(bind=engine)


class M_k(Base):
    __tablename__ = 'm_ks'

    id = Column(Integer, primary_key=True, index=True)                      #
    perelik_id = Column(Integer, ForeignKey("pereliks.id"))
    number = Column(Integer)                                             # Кодування
    resurs = Column(Integer, ForeignKey("pereliks.id"))

    date_created = Column(DateTime(), default=datetime.utcnow)
    date_updated = Column(DateTime(), default=datetime.today)
Base.metadata.create_all(bind=engine)


