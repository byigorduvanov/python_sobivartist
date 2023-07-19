from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

@app.get('/')
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

from routers.zminu import zminu_router
from routers.add_all import add_all_router
from routers.revision import revision_router
from routers.sobivartist import sobivartist_router