from fastapi import APIRouter, FastAPI, Request, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from utils.handle_users_mongo import User_Management
from utils.models import PackageName, UserLogin
from utils.handle_cards_mongo import Card_Management
from utils.handle_packages_mongo import Package_Management
from utils.template_path import templates


router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request, user_id: str = Cookie(None)):
    if user_id:
        return RedirectResponse(url="/home")
    """
    1. Get cards of the user
    2. return them
    """
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/login")
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

@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    """
    1. Get cards of the user
    2. return them
    """
    return templates.TemplateResponse(request=request, name="registration.html")

@router.post("/register")
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


@router.get("/logout", response_class=HTMLResponse)
async def exit_from_app(request: Request, response: Response, user_id: str = Cookie(None)):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie("user_id")
    return response



