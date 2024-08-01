from typing import Any, Sequence

import sqlalchemy

from models.db.ProductDetails import ProductDetails
from repository.crud.base import BaseCRUDRepository
from utils.exceptions.database import EntityDoesNotExist


class ProductDetailCRUDRepository(BaseCRUDRepository):

    async def get_product_by_brand_id(self, brand_id: int) -> list[ProductDetails]:
        stmt = sqlalchemy.select(ProductDetails).where(ProductDetails.brand_id == brand_id)
        query = await self.async_session.execute(statement=stmt)

        results = query.scalars().all()

        if not results:
            raise EntityDoesNotExist(f"Product Detail with brand_id `{brand_id}` does not exist!")

        return list(results)
