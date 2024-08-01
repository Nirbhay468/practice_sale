from datetime import date

from sqlalchemy import select, func, and_

from models.db.CategoryShareData import CategoryShareData
from repository.crud.base import BaseCRUDRepository


class CategoryShareRepository(BaseCRUDRepository):

    async def get_category_market_share_changes(self, start_date: date, end_date: date):
        query = (
            select(
                CategoryShareData.category_id,
                CategoryShareData.date,
                CategoryShareData.market_share
            )
            .where(
                and_(
                    CategoryShareData.date >= start_date,
                    CategoryShareData.date <= end_date
                )
            )
            .order_by(CategoryShareData.category_id, CategoryShareData.date)
        )

        result = await self.async_session.execute(query)
        data = result.fetchall()

        # Calculate the change in market share
        market_share_changes = {}
        for row in data:
            category_id = row.category_id
            if category_id not in market_share_changes:
                market_share_changes[category_id] = {
                    'first': row.market_share,
                    'last': row.market_share
                }
            else:
                market_share_changes[category_id]['last'] = row.market_share

        changes = [
            {
                'category_id': category_id,
                'market_share_change': values['last'] - values['first']
            }
            for category_id, values in market_share_changes.items()
        ]

        return changes
