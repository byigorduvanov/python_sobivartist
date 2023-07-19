from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from database.base import get_db
from main import app, templates
from tables.tables import Collective, Serie, Vavle, Material, Detail, Norm_year, Detail_change, Material_coming
from tables.tables_zero import Specification, Cost

@app.get('/revision')
def revision(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('/revision/index_revision.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )
#=====================ПЕРЕГЛЯД ДЕТАЛЕЙ==============================#
@app.get('/detail_all')
def detailall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('/revision/index_detail_all.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )
#=====================ПЕРЕГЛЯД МАТЕРІАЛУ==============================#
@app.get('/material_all')
def materialall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('/revision/index_material_all.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )
#=====================ПЕРЕГЛЯД СПЕЦИФІКАЦІЯ==============================#
@app.get('/specification')
def specification(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()
    specifications = db_session.query(Specification).all()
    return templates.TemplateResponse('/revision/index_specification.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'collective_list':collectives,
                                       'specification_list':specifications}
                                      )
@app.post('/dele_spec')
def dele_spec(db_session: Session = Depends(get_db)):
    new_specification = db_session.query(Specification).filter(Specification.id > 0)
    for i in new_specification:
        db_session.delete(i)
    db_session.commit()

    url = app.url_path_for('specification')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)
@app.post('/specification')
def specification(A: int = Form(...), db_session: Session = Depends(get_db)):
    for row in db_session.query(Detail, Collective).filter(Collective.detail_id == Detail.id).filter(
            Collective.collective_id == A).group_by(Collective.sequence_number):
        new_Specification = Specification(coding=row.Detail.coding, name=row.Detail.name, number=row.Collective.number)
        db_session.add(new_Specification)
        db_session.commit()
        print(new_Specification.coding, new_Specification.name, new_Specification.number)

    url = app.url_path_for('specification')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
#=====================ПЕРЕЛІК НОРМОГОДИН==============================#
@app.get('/norm_year_all')
def norm_yearall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    norm_years = db_session.query(Norm_year).all()
    return templates.TemplateResponse('/revision/index_norm_year_all.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'norm_year_list': norm_years,}
                                      )