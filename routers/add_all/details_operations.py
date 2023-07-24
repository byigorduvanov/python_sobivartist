from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from database.base import get_db
from main import app, templates
from sqlalchemy import or_, desc, asc
from tables.tables import Detail_Operations

#===================DETAIL OPERATIONS================================#
@app.get('/details_operations')
def detail_operations(request: Request, db_session: Session = Depends(get_db)):
    detail_operations = db_session.query(Detail_Operations).all()
    return templates.TemplateResponse("/details_operations/details_operations.html",
                                     {"request": request, "detail_operations_list": detail_operations})

@app.post('/add_details_operations')
async def add_details_operations(detail_id: int = Form(''), operations_id: int = Form(''), name: str = Form(''), type: str = Form(''), notes: str = Form(''), db_session: Session = Depends(get_db)):
    new_Detail_Operations = Detail_Operations(detail_id = detail_id, operations_id = operations_id, name = name, type = type, notes = notes)
    db_session.add(new_Detail_Operations)
    db_session.commit()
    return new_Detail_Operations

