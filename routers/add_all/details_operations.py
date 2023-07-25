from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from database.base import get_db
from main import app, templates
from sqlalchemy import or_, desc, asc
from tables.tables import Detail_Operations, Detail, Operations


#===================DETAIL OPERATIONS================================#
@app.get('/details_operations')
def detail_operations(request: Request, db_session: Session = Depends(get_db)):
    detail_operations = db_session.query(Detail_Operations).all()
    details = db_session.query(Detail).options(joinedload(Detail.Material)).all()  # Fetch all Details with their Materials
    operations = db_session.query(Operations).all()  # Fetch all Operations
    return templates.TemplateResponse("/details_operations/details_operations.html",
                                      {"request": request,
                                       "detail_operations_list": detail_operations,
                                       "details": details,  # send details to the template
                                       "operations": operations  # send operations to the template
                                      })
@app.post('/add_details_operations')
async def add_details_operations(detail_id: int = Form(''), operations_id: int = Form(''), name: str = Form(''), type: str = Form(''), notes: str = Form(''), db_session: Session = Depends(get_db)):
    new_Detail_Operations = Detail_Operations(detail_id = detail_id, operations_id = operations_id, name = name, type = type, notes = notes)
    db_session.add(new_Detail_Operations)
    db_session.commit()
    return new_Detail_Operations

@app.get('/edit_detail_operations/{detail_operations_id}')
def edit_detail_operations(request: Request, detail_operations_id: int, db_session: Session = Depends(get_db)):
    detail_operations = db_session.query(Detail_Operations).filter_by(id=detail_operations_id).first()
    return templates.TemplateResponse("/details_operations/edit_details_operations.html",
    {"request": request, "detail_operations": detail_operations})
@app.post('/edit_detail_operations/{detail_operations_id}')
def update_detail_operations(request: Request, detail_operations_id: int, detail_id: int = Form(''), operations_id: int = Form(''), name: str = Form(''), type: str = Form(''), notes: str = Form(''), db_session: Session = Depends(get_db)):
    detail_operation = db_session.query(Detail_Operations).filter_by(id=detail_operations_id).first()
    detail_operation.detail_id = detail_id
    detail_operation.operations_id = operations_id
    detail_operation.name = name
    detail_operation.type = type
    detail_operation.notes = notes
    db_session.commit()
    return RedirectResponse(url=app.url_path_for('detail_operations'), status_code=HTTP_303_SEE_OTHER)

@app.get('/search_detail_operations')
def search_detail_operations(request: Request, search_term: str = '', sort_order: str = 'asc', db_session: Session = Depends(get_db)):
    if sort_order == "asc":
        sort_func = asc
    else:
        sort_func = desc
    query = db_session.query(Detail_Operations).join(Detail)
    if search_term:
        query = query.filter(
            or_(Detail.coding.contains(search_term), Detail_Operations.name.contains(search_term), Detail_Operations.type.contains(search_term))
        )
    detail_operations = query.order_by(sort_func(Detail_Operations.date_created)).all()
    details = db_session.query(Detail).options(joinedload(Detail.Material)).all()  # Fetch all Details with their Materials
    operations = db_session.query(Operations).all()  # Fetch all Operations
    return templates.TemplateResponse("/details_operations/details_operations.html",
                                      {"request": request,
                                       "detail_operations_list": detail_operations,
                                       "search_term": search_term,
                                       "sort_order": sort_order,
                                       "details": details,  # send details to the template
                                       "operations": operations  # send operations to the template
                                      })

@app.delete('/delete_detail_operations/{detail_operations_id}')
async def delete_detail_operations(detail_operations_id: int, db_session: Session = Depends(get_db)):
    detail_operation = db_session.query(Detail_Operations).filter_by(id=detail_operations_id).first()
    db_session.delete(detail_operation)
    db_session.commit()
    return {"status": "success", "message": "Detail Operation deleted successfully"}