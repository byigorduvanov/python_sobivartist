from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from database.base import get_db
from main import app, templates
from tables.tables import Collective, Serie, Vavle, Material, Detail, Norm_year, Detail_change, Material_coming
from tables.tables_zero import Specification, Cost


@app.get('/add_all')
def addall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()
    return templates.TemplateResponse('/add_all/index_add_all.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )
#===================матеріали================================#
@app.get('/material')
def material(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    return templates.TemplateResponse('/add_all/index_material.html',
                                     {'request': request,
                                      'material_list': materials}
                                     )
@app.post('/addmaterial')
def addmaterial(marka: str = Form(...), profile: str = Form(...), weight: float = Form(...), price: float = Form(...),db_session: Session = Depends(get_db)):
    new_Material = Material(marka = marka, profile = profile, weight = weight, price = price)
    db_session.add(new_Material)
    db_session.commit()

    url = app.url_path_for('material')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

#===================деталі================================#
@app.get('/detail')
def detail(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('/add_all/index_detail.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials}
                                      )
@app.post('/add_detail')
def add_detail(coding: str = Form(...), name: str = Form(...), product_type: str = Form(...),
              lenght_workpiece: str = Form(...), width_workpiece: str = Form(...), trimming: str = Form(...),
              lenght_detail: str = Form(...), rate_costs: str = Form(...), material_id: int = Form(...),
              db_session: Session = Depends(get_db)):
    new_Detail = Detail(coding=coding, name=name, product_type=product_type, lenght_workpiece=lenght_workpiece,
                        width_workpiece=width_workpiece, trimming=trimming, lenght_detail=lenght_detail,
                        rate_costs=rate_costs, material_id=material_id)

    db_session.add(new_Detail)
    db_session.commit()

    url = app.url_path_for('detail')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#===================покупні деталі================================#
@app.get('/purchase_detail')
def purchase_detail(request: Request, db_session: Session = Depends(get_db)):
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('/add_all/index_purchase_detail.html',
                                      {'request': request,
                                       'detail_list': details}
                                      )
@app.post('/purchase_detail')
def purchase_detail(coding: str = Form(...), name: str = Form(...), price: float = Form(...), db_session: Session = Depends(get_db)):
    product_type = 2
    new_Detail = Detail(coding = coding, name = name, price = price, product_type = product_type)
    db_session.add(new_Detail)
    db_session.commit()

    url = app.url_path_for('purchase_detail')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#=====================ЗБІРНІ ОДИНИЦІ==============================#
@app.get('/collective')
def collective(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()
    return templates.TemplateResponse('/add_all/index_collective.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'collective_list':collectives}
                                      )
@app.post('/collective')
def addcollective(collective_id: int = Form(...), collective_coding:str = Form(...), sequence_number:int = Form(...), detail_id: int = Form(...), number: str = Form(...), db_session: Session = Depends(get_db)):
    Nam = 15145
    new_Collective = Collective(collective_id = collective_id, collective_coding = collective_coding, sequence_number = sequence_number, detail_id = detail_id, number = number)
    db_session.add(new_Collective)
    db_session.commit()

    url = app.url_path_for('collective')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#=====================НОРМИ РІК==============================#
@app.get('/norm_year')
def norm_year(request: Request, db_session: Session = Depends(get_db)):
    details = db_session.query(Detail).all()
    norm_years = db_session.query(Norm_year).all()
    costs = db_session.query(Cost).all()
    return templates.TemplateResponse('/add_all/index_norm_year.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'norm_year_list': norm_years,
                                       'cost_list': costs}
                                      )
@app.post('/norm_year')
def norm_year(detail_id: int = Form(...), norm_years: str = Form(...), norm_year_coding: str = Form(...),
              db_session: Session = Depends(get_db)):
    new_Norm_year = Norm_year(detail_id=detail_id, norm_years=norm_years, norm_year_coding=norm_year_coding)
    db_session.add(new_Norm_year)
    db_session.commit()

    url = app.url_path_for('norm_year')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#=====================ПРИХІД МАТЕРІАЛУ==============================#
@app.get('/material_coming')
def material_coming(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    material_comings = db_session.query(Material_coming).all()
    return templates.TemplateResponse('/add_all/index_material_coming.html',
                                     {'request': request,
                                      'material_list': materials,
                                      'material_coming_list': material_comings}
                                     )
@app.post('/material_coming')
def material_coming(material_id: int = Form(...), price: float = Form(...), availability: float = Form(...), notes: str = Form(...), db_session: Session = Depends(get_db)):
    new_Material_coming = Material_coming(material_id = material_id, price = price, availability = availability, notes = notes)
    db_session.add(new_Material_coming)
    db_session.commit()

    url = app.url_path_for('material_coming')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
