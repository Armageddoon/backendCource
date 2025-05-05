from sqlalchemy import select, func, insert

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()

    async def add_hotel(self, **kwargs):
        query = insert(HotelsOrm).values(**kwargs)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        await self.session.commit()
        last_inserted_id = result.inserted_primary_key[0]
        query = select(HotelsOrm).where(HotelsOrm.id == last_inserted_id)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().first()