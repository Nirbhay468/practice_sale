import sqlalchemy
from typing import List, Optional

from models.db.ProductCategoryMapping import ProductCategoryMapping
from models.db.ProductDetails import ProductDetails
from models.db.SalesData import SalesData
from repository.crud.base import BaseCRUDRepository
from utils.exceptions.database import EntityDoesNotExist
from sqlalchemy import select
from sqlalchemy import func, and_
from datetime import date


class SalesCRUDRepository(BaseCRUDRepository):

    async def get_sales_by_transaction_id(self, transaction_id: int) -> SalesData:
        stmt = sqlalchemy.select(SalesData).where(SalesData.transaction_id == transaction_id)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(f"Sales with transaction_id `{transaction_id}` does not exist!")

        return query.scalar()

    async def get_sales_by_product_ids(self, product_ids: List[int]) -> List[SalesData]:
        stmt = select(SalesData).where(SalesData.product.in_(product_ids))
        query = await self.async_session.execute(statement=stmt)
        sales_data = query.scalars().all()

        if not sales_data:
            raise EntityDoesNotExist(f"Sales with product_ids `{product_ids}` do not exist!")

        return list(sales_data)

    async def get_sales_by_and_date_range(self, start_date: date, end_date: date):
        query = (
            select(
                func.sum(SalesData.quantity).label('total_quantity'),
                func.sum(SalesData.revenue).label('total_revenue')
            )
            .where(
                and_(
                    SalesData.date >= start_date,
                    SalesData.date <= end_date
                )
            )
        )
        result = await self.async_session.execute(query)
        sales_summary = result.all()

        return sales_summary

    async def get_sales_by_fields(
            self,
            group_by_fields: Optional[List[str]] = None
    ):
        base_query = select(
            func.sum(SalesData.quantity).label('total_quantity'),
            func.sum(SalesData.revenue).label('total_revenue')
        )

        # Handle grouping by fields
        if group_by_fields:
            if 'brand' in group_by_fields:
                query = base_query.add_columns(ProductDetails.brand_id.label('brand')).join(
                    ProductDetails, SalesData.product == ProductDetails.product_id
                ).group_by(ProductDetails.brand_id)
            elif 'category' in group_by_fields:
                query = base_query.add_columns(ProductCategoryMapping.category_id.label('category')).join(
                    ProductCategoryMapping, SalesData.product == ProductCategoryMapping.product_id
                ).group_by(ProductCategoryMapping.category_id)
            else:
                if 'product' in group_by_fields:
                    query = base_query.add_columns(SalesData.product.label('product')).group_by(SalesData.product)
        else:
            # Default group by product if no fields are provided
            query = base_query.add_columns(SalesData.product.label('product')).group_by(SalesData.product)

        result = await self.async_session.execute(query)
        sales_summary = result.mappings().all()

        return sales_summary
