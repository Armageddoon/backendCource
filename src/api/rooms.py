from fastapi import Query, APIRouter, Body

from src.repositories.rooms import RoomsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.rooms import RoomPATCH, RoomAdd

router = APIRouter(prefix="/hotels/{hote_id}/rooms", tags=["Номера"])


@router.get("")
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(None, description="Натменование"),
        description: str | None = Query(None, description="Описание"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            description=description
        )


@router.get("/{hotel_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "Эконом",
        "value": {
            "title": "Одноместный эконом",
            "description": "Кровать, тапочки",
        }
    },
    "2": {
        "summary": "Люкс",
        "value": {
            "title": "Одноместный люкс",
            "description": "Кровать двухспальная, тапочки, джакузи",
        }
    }
})
):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": rooms}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}