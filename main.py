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

# app.include_router(cards_router.router)
# app.include_router(package_router.router)
# app.include_router(user_router.router)
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



##################

from fastapi import APIRouter, Request, Cookie

from utils.handle_cards_mongo import Card_Management
from utils.handle_packages_mongo import Package_Management

from  utils.models import Card
from routers.package_router import show_package
from bson.objectid import ObjectId


@app.get("/cards/add_card/{package_id}")
async def show_cards_by_package(
    request: Request, package_id: str, user_id: str = Cookie(None)
):
    card_management = Card_Management()
    cards_data=card_management.get_cards_by_package_id(package_id=package_id)
    package_management = Package_Management()
    package_data = package_management.get_package_by_id(package_id)
    return templates.TemplateResponse(
        request=request,
        name="add_card.html",
        context={"package_data": package_data},
    )

@app.post("/cards/add_card/{package_id}")
async def add_new_card(
    request: Request, package_id: str,card_data:Card, user_id: str = Cookie(None),
):

    card_management = Card_Management()
    card_management.add_card(author_id=user_id,package_id=package_id,
        front=card_data.front,
        back=card_data.back
    )
    return {"success":True}

@app.get("/cards/learn/{package_id}")
async def learn_cards(
    request: Request, package_id: str, user_id: str = Cookie(None),
):

    card_management = Card_Management()
    cards = card_management.get_cards_by_package_id(package_id=package_id)
    for item in cards:
        for k,v in item.items():
            if isinstance(v,ObjectId):
                item[k]=str(v)
    
    print(cards)
    return templates.TemplateResponse(
            request=request,
            name="learn.html",
            context={"cards": cards,"package_id": str(package_id),"iterator":0},
        )

# TODO 2024.12.22 LAST
# TODO html page a cardok felsorolásához
# learn page html


# @router.get("/add_card/{package_id}", response_class=HTMLResponse)
# async def get_add_card(request: Request, package_id: str, user_id: str = Cookie(None)):
#     if check_package_id_valid(package_id):
#         package_data = get_package_by_id(package_id)
#         return templates.TemplateResponse(
#             request=request,
#             name="add_card.html",
#             context={"package_data": package_data},
#         )
#     else:
#         raise StarletteHTTPException

##################
##################

from fastapi import APIRouter, FastAPI, Request, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from utils.handle_users_mongo import User_Management
from utils.models import PackageName, UserLogin
from utils.handle_cards_mongo import Card_Management
from utils.handle_packages_mongo import Package_Management





@app.get("/user/login", response_class=HTMLResponse)
async def get_login(request: Request, user_id: str = Cookie(None)):
    if user_id:
        return RedirectResponse(url="/home")
    """
    1. Get cards of the user
    2. return them
    """
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/user/login")
async def login(response: Response, user: UserLogin):
    user_management = User_Management()
    user_data = user_management.check_user_exists(
        property_name="user_name", property_value=user.username
    )
    if user_data and user.password == user_data.get("password"):
        response.set_cookie(
            key="user_id", value=f"{str(user_data.get("_id"))}", max_age=36000
        )
        return {"success": True, "message": "Login successful!"}
    else:
        return {"success": False, "message": "User not found."}

@app.get("/user/register", response_class=HTMLResponse)
async def get_register(request: Request):
    """
    1. Get cards of the user
    2. return them
    """
    return templates.TemplateResponse(request=request, name="registration.html")

@app.post("/user/register")
async def register(user: UserLogin):
    print(f"Given username: {user.username}")
    user_management = User_Management()
    # user_data=user_management.check_user_exists(property_name="user_name",property_value=user.username)
    # if user_data:
    #     return {"success": False, "message": "Name already exists."}
    # else:
    #     # Add the new user to the registered users list
    result = False
    user_data = None
    try:
        user_data = user_management.add_user(name=user.username, password=user.password)
        message = "Registration successful."
        result = True
    except ValueError as e:
        message = f"Error occured during registration: {e}"
    return {"success": result, "message": message, "user_data": user_data}

@app.get("/user/logout", response_class=HTMLResponse)
async def exit_from_app(request: Request, response: Response, user_id: str = Cookie(None)):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie("user_id")
    return response




##################

from fastapi import APIRouter, FastAPI, Request, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from utils.models import PackageName
from utils.handle_cards_mongo import Card_Management
from utils.handle_packages_mongo import Package_Management




@app.get("/test2", response_class=HTMLResponse)
async def test2(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="test_2.html",
    )

@app.get("/package/create_package", response_class=HTMLResponse)
async def create_package_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_new_package.html",
    )


@app.post("/package/create_package")
async def create_package(
    response: Response, package_name: PackageName, user_id: str = Cookie(None)
):
    package_management = Package_Management()
    package_data = package_management.add_package(
        package_name=package_name.package_name, author_id=user_id
    )
    if package_data:
        return {"success": True, "message": "Package creation successful!"}
    else:
        return {"success": False, "message": "Package already exists"}




@app.get("/package/{package_id}")
async def show_package(request: Request, package_id: str, user_id: str = Cookie(None)):
    
    card_management = Card_Management()
    cards_data=card_management.get_cards_by_package_id(package_id=package_id)
    package_management = Package_Management()
    package_data = package_management.get_package_by_id(package_id)
    print(package_data)
    return templates.TemplateResponse(
            request=request,
            name="show_package.html",
            context={"package_data":package_data,"card_data": cards_data},
        )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
