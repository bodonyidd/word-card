from fastapi import Cookie, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.handle_packages_mongo import Package_Management
from utils.handle_users_mongo import User_Management
from routers import cards_router
from routers import package_router
from routers import user_router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(cards_router.router)
app.include_router(package_router.router)
app.include_router(user_router.router)
app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")


# JinjaTemplates
# from utils.template_path import templates


@app.get("/", response_class=HTMLResponse)
async def slash(request: Request):
    """
    1. Get cards of the user
    2. return them
    """
    return templates.TemplateResponse(request=request, name="landing_page.html")


@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    """
    1. Get cards of the user
    2. return them
    """
    return templates.TemplateResponse(request=request, name="test_1.html")


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, user_id: str = Cookie(None)):
    """
    1. Get packages of the user
    2. return them
    """
    package_management = Package_Management()
    packages_by_user = package_management.get_packages_by_author(author_id=user_id)
    user_data = User_Management().check_user_exists(
        property_name="_id", property_value=user_id
    )
    if user_data == False:
        user_router.get_login(request=Request)
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"packages": packages_by_user, "username": user_data.get("user_name")},
    )


@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
    return HTMLResponse(f"<h1>{exc.detail}</h1>", status_code=exc.status_code)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
