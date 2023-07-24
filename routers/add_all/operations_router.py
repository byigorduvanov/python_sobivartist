from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from database.base import get_db
from main import app, templates
from tables.tables import Operations
from sqlalchemy import or_, desc, asc
#===================ОПЕРАЦІЇ================================#
@app.get('/operations')
def operations(request: Request, db_session: Session = Depends(get_db)):
    operations = db_session.query(Operations).all()
    return templates.TemplateResponse("/operations/operations.html",
                                     {"request": request, "operations_list": operations})
@app.post('/add_operations')
async def add_operations(coding: str = Form(''), name: str = Form(''), type: str = Form(''), notes: str = Form(''), db_session: Session = Depends(get_db)):
    new_Operations = Operations(coding = coding, name = name, type = type, notes = notes)
    db_session.add(new_Operations)
    db_session.commit()
    return new_Operations
@app.get('/edit_operation/{operation_id}')
def edit_operation(request: Request, operation_id: int, db_session: Session = Depends(get_db)):
    operation = db_session.query(Operations).filter_by(id=operation_id).first()
    return templates.TemplateResponse("/operations/edit_operation.html", {"request": request, "operation": operation})

@app.post('/edit_operation/{operation_id}')
def update_operation(request: Request, operation_id: int, coding: str = Form(''), name: str = Form(''), type: str = Form(''), notes: str = Form(''), db_session: Session = Depends(get_db)):
    operation = db_session.query(Operations).filter_by(id=operation_id).first()
    operation.coding = coding
    operation.name = name
    operation.type = type
    operation.notes = notes
    db_session.commit()
    return RedirectResponse(url=app.url_path_for('operations'), status_code=HTTP_303_SEE_OTHER)


@app.get('/search_operations')
def search_operations(request: Request, search_term: str = '', sort_order: str = 'asc', db_session: Session = Depends(get_db)):
    if sort_order == "asc":
        sort_func = asc
    else:
        sort_func = desc

    query = db_session.query(Operations)

    if search_term:
        query = query.filter(
            or_(Operations.coding.contains(search_term), Operations.name.contains(search_term))
        )

    operations = query.order_by(sort_func(Operations.date_created)).all()

    return templates.TemplateResponse("/operations/operations.html",
                                      {"request": request, "operations_list": operations, "search_term": search_term, "sort_order": sort_order})
@app.delete('/delete_operation/{operation_id}')
async def delete_operation(operation_id: int, db_session: Session = Depends(get_db)):
    operation = db_session.query(Operations).filter_by(id=operation_id).first()
    db_session.delete(operation)
    db_session.commit()
    return {"status": "success", "message": "Operation deleted successfully"}

