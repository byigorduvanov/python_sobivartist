from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, Float, VARCHAR, Sequence
from database.base import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime

class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, Sequence('materials_id_seq'), primary_key=True, index=True)
    marka = Column(String)                                                  # Марка матеріалу
    profile = Column(String)                                                # Профіль
    weight = Column(Float)                                                   # Вага п/м
    price = Column(Float)                                                    # Ціна за 1т.
    notes = Column(String)                                                  #
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
Base.metadata.create_all(bind=engine)
class Detail(Base):
    __tablename__ = 'details'
    id = Column(Integer, Sequence('details_id_seq'), primary_key=True, index=True)
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
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)

    Material = relationship("Material")
    detail_m_ks = relationship('Detail_m_k', back_populates='detail')
Base.metadata.create_all(bind=engine)
class Detail_change(Base):
    __tablename__ = 'detail_changes'
    id = Column(Integer, Sequence('detail_changes_id_seq'), primary_key=True, index=True)
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
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
Base.metadata.create_all(bind=engine)
class Serie(Base):
    __tablename__ = 'series'
    id = Column(Integer, Sequence('series_id_seq'), primary_key=True, index=True)
    name_serie = Column(String)                                             # Назва серії кранів
    notes = Column(String)                                                  # 
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
Base.metadata.create_all(bind=engine)
class Vavle(Base):
    __tablename__ = 'vavles'
    id = Column(Integer, Sequence('vavles_id_seq'), primary_key=True, index=True)
    serie_id = Column(Integer, ForeignKey("series.id"))                     #
    detail_id = Column(Integer, ForeignKey("details.id"))                   #
    Serie = relationship("Serie")
    Detail = relationship("Detail")
    notes = Column(String)
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
Base.metadata.create_all(bind=engine)
class Collective(Base):
    __tablename__ = 'colectives'
    id = Column(Integer, Sequence('colectives_id_seq'), primary_key=True, index=True)
    collective_id = Column(Integer, ForeignKey("details.id"))               #
    collective_coding = Column(VARCHAR(13))                                 # Кодування
    sequence_number = Column(Integer)                                       # Порядковий номер
    detail_id = Column(Integer)                                             # Кодування деталі    
    number = Column(Float)                                                  # Кількість деталей в зборці
    notes = Column(String)                                                  # 
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)         
    Detail = relationship("Detail")
Base.metadata.create_all(bind=engine)
class Norm_year(Base):
    __tablename__ = 'norm_years'
    id = Column(Integer, Sequence('norm_years_id_seq'), primary_key=True, index=True)                    #
    detail_id = Column(Integer, ForeignKey("details.id"))                   #
    norm_year_coding = Column(VARCHAR(13))                                  # Кодування        
    norm_years = Column(Float)                                              # Нормо-годин
    notes = Column(String)                                                  # 
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)         
    Detail = relationship("Detail")
Base.metadata.create_all(bind=engine)

class Material_coming(Base):
    __tablename__ = 'material_comings'
    id = Column(Integer, Sequence('material_comings_id_seq'), primary_key=True, index=True)
    material_id = Column (Integer, ForeignKey("materials.id"))
    price = Column(Float)
    availability = Column (Float)                                           # Кількість приходу
    notes = Column(String)                                                  # Номер документу (Накладна, партія)
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
    Material = relationship("Material")
Base.metadata.create_all(bind=engine)

# ===============ПО ОПЕРАЦІЙНО======================#
class Detail_m_k(Base):
    __tablename__ = 'detail_m_k'
    id = Column(Integer, primary_key=True, index=True)
    detail_id = Column(Integer, ForeignKey("details.id"))
    detail_operations_id = Column(Integer, ForeignKey("detail_operations.id"))
    seqence = Column(Integer)
    name = Column(String)
    notes = Column(String)
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)

    detail = relationship('Detail', back_populates='detail_m_ks')
    detail_operations = relationship('Detail_Operations')
Base.metadata.create_all(bind=engine)

class Operations(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True, index=True)
    coding = Column(String)
    name = Column(String)
    type = Column(String)
    notes = Column(String)
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
Base.metadata.create_all(bind=engine)

class Detail_Operations(Base):
    __tablename__ = 'detail_operations'
    id = Column(Integer, primary_key=True, index=True)
    detail_id = Column(Integer, ForeignKey("details.id"))
    operations_id = Column(Integer, ForeignKey("operations.id"))
    name = Column(String)
    type = Column(String)
    notes = Column(String)
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)

    detail = relationship("Detail", backref="detail_operations")
    operations = relationship("Operations", backref="detail_operations")
    detail_m_ks = relationship('Detail_m_k', back_populates='detail_operations')
Base.metadata.create_all(bind=engine)
class Normu_kilkist(Base):
    __tablename__ = 'normu_kilkist'
    id = Column(Integer, primary_key=True, index=True)
    id_operations = Column(Integer, ForeignKey("operations.id"))
    kilkist = Column(String)
    name = Column(String)
    notes = Column(String)
    date_created = Column(DateTime, default=datetime.today)
    date_updated = Column(DateTime, default=datetime.today, onupdate=datetime.today)
Base.metadata.create_all(bind=engine)