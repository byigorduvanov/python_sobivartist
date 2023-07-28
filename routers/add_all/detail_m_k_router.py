from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session, joinedload
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from database.base import get_db
from main import app, templates
from sqlalchemy import or_, desc, asc
from tables.tables import Detail_m_k, Detail, Detail_Operations

@app.get('/detail_m_k')
def detail_m_k(request: Request, db_session: Session = Depends(get_db)):
    detail_m_k = db_session.query(Detail_m_k).options(joinedload(Detail_m_k.detail)).all()
    details = db_session.query(Detail).options(joinedload(Detail.Material)).all()
    detail_operations = db_session.query(Detail_Operations).all()
    return templates.TemplateResponse("/detail_m_k/detail_m_k.html",
                                      {"request": request,
                                       "detail_m_k_list": detail_m_k,
                                       "details": details,
                                       "detail_operations": detail_operations})

@app.post('/add_detail_m_k')
async def add_detail_m_k(request: Request, db_session: Session = Depends(get_db)):
    form = await request.form()

    # Get a list of indices from the form fields
    indices = set(int(key.split('_')[-1]) for key in form.keys() if key.startswith('detail_id_'))

    for index in indices:
        detail_id = form.get(f'detail_id_{index}')
        detail_operations_id = form.get(f'detail_operations_id_{index}')
        seqence = form.get(f'seqence_{index}')
        name = form.get('name')
        notes = form.get('notes')

        new_detail_m_k = Detail_m_k(detail_id=detail_id, detail_operations_id=detail_operations_id, seqence=seqence, name=name, notes=notes)
        db_session.add(new_detail_m_k)

    db_session.commit()
    return RedirectResponse(url=app.url_path_for('detail_m_k'), status_code=HTTP_303_SEE_OTHER)


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
    detail_m_k = db_session.query(Detail_m_k).filter_by(id=detail_m_k_id).first()
    db_session.delete(detail_m_k)
    db_session.commit()
    return {"status": "success", "message": "Detail_m_k deleted successfully"}
