from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from database.base import get_db
from main import app, templates
from tables.tables import Collective, Serie, Vavle, Material, Detail, Norm_year, Detail_change, Material_coming
from tables.tables_zero import Specification, Cost
import pandas as pd
from openpyxl import load_workbook


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/updetdetail')
def updetdetail(request: Request, db_session: Session = Depends(get_db)):
    details = db_session.query(Detail).all()
    materials = db_session.query(Material).all()
    detail_changes = db_session.query(Detail_change).all()
    return templates.TemplateResponse('index_updetdetail.html',
                                      {'request': request,
                                       'material_list': materials,                                      
                                       'detail_list': details,
                                       'detail_change_list': detail_changes}
                                      )
@app.get('/norm_year')
def norm_year(request: Request, db_session: Session = Depends(get_db)):
    details = db_session.query(Detail).all()
    norm_years = db_session.query(Norm_year).all()
    costs = db_session.query(Cost).all()
    return templates.TemplateResponse('index_norm_year.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'norm_year_list': norm_years,
                                       'cost_list': costs}
                                      )
@app.get('/specification')
def specification(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()   
    specifications = db_session.query(Specification).all()   
    return templates.TemplateResponse('index_specification.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'collective_list':collectives,
                                       'specification_list':specifications}
                                      )
@app.get('/collective')
def collective(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()   
    return templates.TemplateResponse('index_collective.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'collective_list':collectives}
                                      )

@app.get('/detail')
def detail(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('index_detail.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials}
                                      )

@app.get('/purchase_detail')
def purchase_detail(request: Request, db_session: Session = Depends(get_db)):
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('index_purchase_detail.html',
                                      {'request': request,
                                       'detail_list': details}
                                      )                                      


@app.get('/cost')
def cost(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()
    series = db_session.query(Serie).all()
    vavles = db_session.query(Vavle).all()
    specifications = db_session.query(Specification).all()
    costs = db_session.query(Cost).all()    
    return templates.TemplateResponse('index_cost.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'collective_list':collectives,
                                       'specification_list':specifications,
                                       'cost_list': costs}
                                      )


@app.get('/addall')
def addall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    collectives = db_session.query(Collective).all()
    return templates.TemplateResponse('index_addall.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )


@app.get('/zminu')
def zminu(request: Request, db_session: Session = Depends(get_db)):
    return templates.TemplateResponse('index_zminu.html',
                                      {'request': request}
                                      )

@app.get('/detailall')
def detailall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('index_detailall.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )


@app.get('/materialall')
def materialall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('index_materialall.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )                            


@app.get('/norm_yearall')
def norm_yearall(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    norm_years = db_session.query(Norm_year).all()
    return templates.TemplateResponse('index_norm_yearall.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,
                                       'norm_year_list': norm_years,}
                                      )                 

@app.get('/revision')
def revision(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    details = db_session.query(Detail).all()
    return templates.TemplateResponse('index_revision.html',
                                      {'request': request,
                                       'detail_list': details,
                                       'material_list': materials,}
                                      )

@app.get('/material')
def material(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    return templates.TemplateResponse('index_material.html',
                                     {'request': request,
                                      'material_list': materials}
                                     )


@app.get('/material_coming')
def material_coming(request: Request, db_session: Session = Depends(get_db)):
    materials = db_session.query(Material).all()
    material_comings = db_session.query(Material_coming).all()    
    return templates.TemplateResponse('index_material_coming.html',
                                     {'request': request,
                                      'material_list': materials,
                                      'material_coming_list': material_comings}
                                     )


@app.post('/adddetail')
def adddetail(coding: str = Form(...), name: str = Form(...), product_type: str = Form(...), lenght_workpiece: str = Form(...), width_workpiece: str = Form(...), trimming: str = Form(...), lenght_detail: str = Form(...), rate_costs: str = Form(...),  material_id: int = Form(...), db_session: Session = Depends(get_db)):
    new_Detail = Detail(coding = coding, name = name, product_type = product_type, lenght_workpiece = lenght_workpiece, width_workpiece = width_workpiece, trimming = trimming, lenght_detail = lenght_detail, rate_costs = rate_costs, material_id = material_id)

    
    db_session.add(new_Detail)
    db_session.commit()

    url = app.url_path_for('detail')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/purchase_detail')
def purchase_detail(coding: str = Form(...), name: str = Form(...), price: float = Form(...), db_session: Session = Depends(get_db)):
    product_type = 2
    new_Detail = Detail(coding = coding, name = name, price = price, product_type = product_type)
    db_session.add(new_Detail)
    db_session.commit()

    url = app.url_path_for('purchase_detail')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/printdetail')
def printdetail(db_session: Session = Depends(get_db)):
    for row in db_session.query(Detail, Material).filter(Detail.material_id == Material.id).group_by(Detail.coding):
        Sp = (row.Detail.coding, row.Detail.name, row.Material.marka,  row.Material.profile, row.Material.weight, row.Material.price)
        print(Sp)


    url = app.url_path_for('proba')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/addmaterial')
def addmaterial(marka: str = Form(...), profile: str = Form(...), weight: float = Form(...), price: float = Form(...),db_session: Session = Depends(get_db)):
    new_Material = Material(marka = marka, profile = profile, weight = weight, price = price)
    db_session.add(new_Material)
    db_session.commit()   

    url = app.url_path_for('material')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)








@app.post('/collective')
def addcollective(collective_id: int = Form(...), collective_coding:str = Form(...), sequence_number:int = Form(...), detail_id: int = Form(...), number: str = Form(...), db_session: Session = Depends(get_db)):
    Nam = 15145
    new_Collective = Collective(collective_id = collective_id, collective_coding = collective_coding, sequence_number = sequence_number, detail_id = detail_id, number = number)
    db_session.add(new_Collective)
    db_session.commit()

    url = app.url_path_for('collective')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/specification')
def specification(A:int = Form(...), db_session: Session = Depends(get_db)):
    for row in db_session.query(Detail, Collective).filter(Collective.detail_id == Detail.id).filter(Collective.collective_id == A).group_by(Collective.sequence_number):
        new_Specification = Specification(coding = row.Detail.coding, name = row.Detail.name, number = row.Collective.number)
        db_session.add(new_Specification)
        db_session.commit()
        print(new_Specification.coding, new_Specification.name, new_Specification.number)
       

    url = app.url_path_for('specification')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/dele_spec')
def dele_spec(db_session: Session = Depends(get_db)):
    new_specification = db_session.query(Specification).filter(Specification.id > 0)
    for i in new_specification:
        db_session.delete(i)
    db_session.commit()

    url = app.url_path_for('specification')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@app.post('/cost')
def cost(A:int = Form(...), db_session: Session = Depends(get_db)):
   # new_collective_id = Collective(collective_id = A)
    for row in db_session.query(Detail, Collective, Material, Norm_year).filter(Collective.detail_id == Detail.id, Detail.material_id == Material.id, Norm_year.detail_id == Detail.id).filter(Collective.collective_id == A).group_by(Collective.sequence_number):
        rate_costs = round(((row.Material.weight /1000) * row.Detail.rate_costs), 4)
        rates_costs = rate_costs * row.Collective.number
  
        if row.Detail.price == 0:
            cost_materials = round((rates_costs * (row.Material.price /1000)), 2)                  
        else:
            cost_materials = row.Detail.price   
        norms_years = round(row.Norm_year.norm_years * row.Collective.number, 4)
        norms_sec = round(norms_years * 3600, 2)
        price_kg = round((row.Material.price /1000), 3)
   
       
        new_Cost = Cost(coding = row.Detail.coding, name = row.Detail.name, number = row.Collective.number, marka = row.Material.marka, profile = row.Material.profile, rate_costs = rate_costs, rates_costs = rates_costs, cost_materials = cost_materials, norm_years = row.Norm_year.norm_years, norms_years = norms_years, norms_sec = norms_sec, price_kg = price_kg)
        db_session.add(new_Cost)
        db_session.commit()

    url = app.url_path_for('cost')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/dele_cost')
def dele_cost( db_session: Session = Depends(get_db)):
    db_session.query(Cost).filter(Cost.id > 0).delete(synchronize_session="fetch")
    db_session.commit()
    
    url = app.url_path_for('cost')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@app.post('/excel')
def excel(A:int = Form(...), db_session: Session = Depends(get_db)):
    #new_collective_id = Collective(collective_id = A)
    for row in db_session.query(Detail, Collective, Material, Norm_year).filter(Collective.detail_id == Detail.id, Detail.material_id == Material.id, Norm_year.detail_id == Detail.id).filter(Collective.collective_id == A).group_by(Collective.sequence_number):
        rate_costs = round(((row.Material.weight /1000) * row.Detail.rate_costs), 4)
        rates_costs = rate_costs * row.Collective.number
  
        if row.Detail.price == 0:
            cost_materials = round((rates_costs * (row.Material.price /1000)), 2)                  
        else:
            cost_materials = row.Detail.price   
        norms_years = round(row.Norm_year.norm_years * row.Collective.number, 4)
        norms_sec = round(norms_years * 3600, 2)
        price_kg = round((row.Material.price /1000), 3)
         
         
        #ПЕРЕЗАПИСУЄ ДАННІ 
        df = pd.DataFrame([row.Detail.coding, row.Detail.name, row.Collective.number, row.Material.marka, row.Material.profile, rate_costs, rates_costs, row.Norm_year.norm_years, cost_materials, norms_years, norms_sec, price_kg])
        df.to_excel('cost.xlsx')
        
        #ДОДАЄ ДАННІ
        wb = load_workbook('data1.xlsx')
        ws = wb['data']           
        ws.append([row.Detail.coding, row.Detail.name, row.Collective.number, row.Material.marka, row.Material.profile, rate_costs, rates_costs, row.Norm_year.norm_years, cost_materials, norms_years, norms_sec, price_kg])
        wb.save('data1.xlsx')
        wb.close() 

    url = app.url_path_for('cost')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@app.post('/norm_year')
def norm_year(detail_id: int = Form(...), norm_years: str = Form(...), norm_year_coding: str = Form(...), db_session: Session = Depends(get_db)):
    new_Norm_year = Norm_year (detail_id = detail_id, norm_years = norm_years, norm_year_coding = norm_year_coding)
    db_session.add(new_Norm_year)
    db_session.commit()
       
    url = app.url_path_for('norm_year')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/updatedetail')
def updatedetail(detail_id: int, db_session: Session = Depends(get_db)):
    detail = db_session.query(Detail).filter(Detail.id == detail_id).first()
    detail.is_complete = not detail.is_complete
    db_session.commit()

    url = app.url_path_for('updatedetail')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)



@app.post('/updetdetail')
def updetdetail( A:int = Form(...), second_coding:str = Form(None), second_name:str = Form(None), second_product_type:str = Form(None), second_lenght_workpiece:str = Form(None), second_width_workpiece:str = Form(None), second_trimming:str = Form(None), second_lenght_detail:str = Form(None), second_rate_costs:str = Form(None), second_material_id:str = Form(None), db_session: Session = Depends(get_db)):
    second_detail = db_session.query(Detail).filter_by(id=A).one()
    for row in db_session.query(Detail):
        if row.id == A:
            new_Detail_change = Detail_change(detail_id = row.id, coding = row.coding, name = row.name, product_type = row.product_type, lenght_workpiece = row.lenght_workpiece, width_workpiece = row.width_workpiece, trimming = row.trimming, lenght_detail = row.lenght_detail, rate_costs = row.rate_costs, notes = row.notes, price = row.price, material_id = row.material_id, date_created = row.date_created, date_updated = row.date_updated)
            db_session.add(new_Detail_change)
            db_session.commit() 

    second_detail = db_session.query(Detail).filter_by(id=A).one()   
    if second_detail != []:
        if second_coding == None:
            second_detail.coding = Detail.coding
        else: 
            second_detail.coding = second_coding
        
        if second_name == None:
            second_detail.name = Detail.name
        else: 
            second_detail.name = second_name        

        if second_product_type == None:
            second_detail.product_type = Detail.product_type
        else: 
            second_detail.product_type = second_product_type    

        if second_lenght_workpiece == None:
            second_detail.lenght_workpiece = Detail.lenght_workpiece
        else: 
            second_detail.lenght_workpiece = second_lenght_workpiece        

        if second_width_workpiece == None:
            second_detail.width_workpiece = Detail.width_workpiece
        else: 
            second_detail.width_workpiece = second_width_workpiece

        if second_trimming == None:
            second_detail.trimming = Detail.trimming
        else: 
            second_detail.trimming = second_trimming

        if second_lenght_detail == None:
            second_detail.lenght_detail = Detail.lenght_detail
        else: 
            second_detail.lenght_detail = second_lenght_detail

        if second_rate_costs == None:
            second_detail.rate_costs = Detail.rate_costs
        else: 
            second_detail.rate_costs = second_rate_costs

        if second_material_id == None:
            second_detail.material_id = Detail.material_id
        else: 
            second_detail.material_id = second_material_id        

        db_session.add(second_detail)
        db_session.commit()

    url = app.url_path_for('updetdetail')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.post('/material_coming')
def material_coming(material_id: int = Form(...), price: float = Form(...), availability: float = Form(...), notes: str = Form(...), db_session: Session = Depends(get_db)):
    new_Material_coming = Material_coming(material_id = material_id, price = price, availability = availability, notes = notes)
    db_session.add(new_Material_coming)
    db_session.commit()   

    url = app.url_path_for('material_coming')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)