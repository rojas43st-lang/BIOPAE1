from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carpeta templates
templates = Jinja2Templates(directory="templates")


# INICIO DE SESIÓN
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# MENÚ PRINCIPAL
@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={
            "request": request
        }
    )

# VASO DE LECHE
@app.get("/vaso", response_class=HTMLResponse)
async def vaso(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="vaso.html",
        context={
            "request": request
        }
    )

# ALMUERZOS
@app.get("/almuerzo", response_class=HTMLResponse)
async def almuerzo(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="almuerzo.html",
        context={
            "request": request
        }
    )