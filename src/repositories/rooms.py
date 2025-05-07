from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
        self,
        hotel_id,
        title,
        description,
    ) -> list[Room]:
        query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()


