from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from database.base import get_db
from main import app, templates
from tables.tables import Collective, Serie, Vavle, Material, Detail, Norm_year, Detail_change, Material_coming
from openpyxl import load_workbook


@app.get('/zminu')
def zminu(request: Request, db_session: Session = Depends(get_db)):
    return templates.TemplateResponse('/zminu/index_zminu.html',
                                      {'request': request}
                                      )
#=====================ЗМІНА ДЕТАЛІ==============================#
@app.get('/updetdetail')
def updetdetail(request: Request, db_session: Session = Depends(get_db)):
    details = db_session.query(Detail).all()
    materials = db_session.query(Material).all()
    detail_changes = db_session.query(Detail_change).all()
    return templates.TemplateResponse('/zminu/index_updetdetail.html',
                                      {'request': request,
                                       'material_list': materials,
                                       'detail_list': details,
                                       'detail_change_list': detail_changes}
                                      )

@app.post('/updetdetail')
def updetdetail(
        A: int = Form(...),
        second_coding: str = Form(None),
        second_name: str = Form(None),
        second_product_type: str = Form(None),
        second_lenght_workpiece: str = Form(None),
        second_width_workpiece: str = Form(None),
        second_trimming: str = Form(None),
        second_lenght_detail: str = Form(None),
        second_rate_costs: str = Form(None),
        second_material_id: str = Form(None),
        db_session: Session = Depends(get_db),
):
    # Fetch the detail record
    second_detail = db_session.query(Detail).filter_by(id=A).one()

    # Add old detail record to Detail_change table
    new_Detail_change = Detail_change(
        detail_id=second_detail.id,
        coding=second_detail.coding,
        name=second_detail.name,
        product_type=second_detail.product_type,
        lenght_workpiece=second_detail.lenght_workpiece,
        width_workpiece=second_detail.width_workpiece,
        trimming=second_detail.trimming,
        lenght_detail=second_detail.lenght_detail,
        rate_costs=second_detail.rate_costs,
        notes=second_detail.notes,
        price=second_detail.price,
        material_id=second_detail.material_id,
        date_created=second_detail.date_created,
        date_updated=second_detail.date_updated,
    )
    db_session.add(new_Detail_change)

    # Update fields of the detail record
    second_detail.coding = second_coding or second_detail.coding
    second_detail.name = second_name or second_detail.name
    second_detail.product_type = second_product_type or second_detail.product_type
    second_detail.lenght_workpiece = second_lenght_workpiece or second_detail.lenght_workpiece
    second_detail.width_workpiece = second_width_workpiece or second_detail.width_workpiece
    second_detail.trimming = second_trimming or second_detail.trimming
    second_detail.lenght_detail = second_lenght_detail or second_detail.lenght_detail
    second_detail.rate_costs = second_rate_costs or second_detail.rate_costs
    second_detail.material_id = second_material_id or second_detail.material_id

    db_session.add(second_detail)
    db_session.commit()

    url = app.url_path_for('updetdetail')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)