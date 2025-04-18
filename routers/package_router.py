from fastapi import APIRouter, FastAPI, Request, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from utils.models import PackageName
from utils.handle_cards_mongo import Card_Management
from utils.handle_packages_mongo import Package_Management
from utils.template_path import templates


router = APIRouter(
    prefix="/package",
    tags=["package"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/test2", response_class=HTMLResponse)
async def test2(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="test_2.html",
    )

@router.get("/create_package", response_class=HTMLResponse)
async def create_package_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_new_package.html",
    )


@router.post("/create_package")
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




@router.get("/{package_id}")
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