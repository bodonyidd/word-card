from fastapi import APIRouter, Request, Cookie

from utils.handle_cards_mongo import Card_Management
from utils.handle_packages_mongo import Package_Management
from utils.template_path import templates
from  utils.models import Card
from routers.package_router import show_package
from bson.objectid import ObjectId

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/add_card/{package_id}")
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

@router.post("/add_card/{package_id}")
async def add_new_card(
    request: Request, package_id: str,card_data:Card, user_id: str = Cookie(None),
):

    card_management = Card_Management()
    card_management.add_card(author_id=user_id,package_id=package_id,
        front=card_data.front,
        back=card_data.back
    )
    return {"success":True}

@router.get("/learn/{package_id}")
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
