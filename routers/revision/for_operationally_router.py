from fastapi import Request, Depends, Form, Request
from sqlalchemy.orm import Session
from database.base import get_db
from main import app, templates
from tables.tables import Collective,Material, Detail, Detail_m_k, Operations, Detail_Operations



@app.get('/for_operationally')
def for_operationally(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('/revision/for_operationally.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                      })


@app.post('/for_operationally')
def post_for_operationally(request: Request, A: str = Form(...), db_session: Session = Depends(get_db)):
    detail_id = int(A.split(' ')[0])
    detail_m_k_data = db_session.query(Detail_m_k).filter(Detail_m_k.detail_id == detail_id).order_by(
        Detail_m_k.seqence).all()

    # Fetch detail_list and material_list
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()

    # Fetch detail_list and material_list
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()

    return templates.TemplateResponse('/revision/for_operationally.html',
                                      {'request': request,
                                       'detail_m_k_list': detail_m_k_data,
                                       'detail_list': details,  # Add this line
                                       'material_list': materials  # Add this line
                                       }
                                      )

