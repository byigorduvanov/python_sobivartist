from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from database.base import get_db
from main import app, templates
from sqlalchemy import or_, desc, asc
from tables.tables import Detail_m_k, Detail, Detail_Operations, Operations

@app.get('/detail_m_k')
def detail_m_k(request: Request, db_session: Session = Depends(get_db)):
    detail_m_k = db_session.query(Detail_m_k).options(joinedload(Detail_m_k.detail)).all()
    details = db_session.query(Detail).options(joinedload(Detail.Material)).all()
    detail_operations = db_session.query(Detail_Operations).all()
    operations = db_session.query(Operations).all()
    return templates.TemplateResponse("/detail_m_k/detail_m_k.html",
                                      {"request": request,
                                       "detail_m_k_list": detail_m_k,
                                       "details": details,
                                       "operations": operations,
                                       "detail_operations": detail_operations})

@app.post('/add_detail_m_k')
async def add_detail_m_k(request: Request, db_session: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    notes = form.get("notes")

    main_detail_id = form.get("detail_id")  # This is the detail_id for Detail_m_k
    detail_operations_ids = form.getlist("detail_operations_id[]")  # This is for Detail_Operations
    operations_ids = form.getlist("operations_id[]")
    seqence = form.getlist("sequence[]")

    # For each operation, create a new DetailOperation and a new DetailMK
    for detail_operations_id, operations_id, seqence in zip(detail_operations_ids, operations_ids, seqence):
        # Create new DetailOperation
        detail_operation = Detail_Operations(detail_id=detail_operations_id, operations_id=operations_id, name="", type="", notes="")
        db_session.add(detail_operation)
        db_session.commit()

        # Create new DetailMK with detail_operations_id from the newly created DetailOperation
        detail_mk = Detail_m_k(detail_id=main_detail_id, name=name, notes=notes, seqence=seqence, detail_operations_id=detail_operation.id)

        db_session.add(detail_mk)
        db_session.commit()

    return RedirectResponse(url='/detail_m_k', status_code=HTTP_303_SEE_OTHER)


@app.get('/edit_detail_m_k/{detail_m_k_id}')
def edit_detail_m_k(request: Request, detail_m_k_id: int, db_session: Session = Depends(get_db)):
    detail_m_k = db_session.query(Detail_m_k).filter(Detail_m_k.id == detail_m_k_id).first()  # Get the specific Detail_m_k object
    details = db_session.query(Detail).options(joinedload(Detail.Material)).all()
    detail_operations = db_session.query(Detail_Operations).all()
    return templates.TemplateResponse("/detail_m_k/edit_detail_m_k.html",
                                      {"request": request,
                                       "detail_m_k": detail_m_k,  # Pass the specific Detail_m_k object
                                       "details": details,
                                       "detail_operations": detail_operations})


@app.post('/edit_detail_m_k/{detail_m_k_id}')
def update_detail_m_k(request: Request, detail_m_k_id: int, detail_id: int = Form(''), detail_operations_id: int = Form(''), seqence: int = Form(''), name: str = Form(''), notes: str = Form(''), db_session: Session = Depends(get_db)):
    detail_m_k = db_session.query(Detail_m_k).filter_by(id=detail_m_k_id).first()
    detail_m_k.detail_id = detail_id
    detail_m_k.detail_operations_id = detail_operations_id
    detail_m_k.seqence = seqence
    detail_m_k.name = name
    detail_m_k.notes = notes
    db_session.commit()
    return RedirectResponse(url=app.url_path_for('detail_m_k'), status_code=HTTP_303_SEE_OTHER)

@app.delete('/delete_detail_m_k/{detail_m_k_id}')
async def delete_detail_m_k(detail_m_k_id: int, db_session: Session = Depends(get_db)):
    # Get Detail_m_k record
    detail_m_k = db_session.query(Detail_m_k).filter_by(id=detail_m_k_id).first()

    # Get corresponding Detail_Operations record
    detail_operation_id = detail_m_k.detail_operations_id
    detail_operation = db_session.query(Detail_Operations).filter_by(id=detail_operation_id).first()

    # Delete Detail_m_k record
    db_session.delete(detail_m_k)
    db_session.commit()

    # Delete Detail_Operations record
    db_session.delete(detail_operation)
    db_session.commit()

    return {"status": "success", "message": "Detail_m_k and corresponding Detail_Operations record deleted successfully"}

