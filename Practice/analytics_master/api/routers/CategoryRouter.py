from fastapi import APIRouter, Depends, Query, HTTPException, status
from datetime import date
import loguru

from models.schemas.CategoryShareResponse import CategoryMarketShareChangeResponse, CategoryMarketShareChange
from repository.crud.categoryShare import CategoryShareRepository
from api.dependencies.repository import get_repository

router = APIRouter()

@router.get(
    path="/market-share-changes",
    name="market-share:get-market-share-changes",
    response_model=CategoryMarketShareChangeResponse,
    status_code=status.HTTP_200_OK,
)
async def get_market_share_changes(
        start_date: date = Query(..., description="Start date for the market share change period"),
        end_date: date = Query(..., description="End date for the market share change period"),
        category_share_repo: CategoryShareRepository = Depends(get_repository(repo_type=CategoryShareRepository))
) -> CategoryMarketShareChangeResponse:
    loguru.logger.info(f"Received request for market share changes from {start_date} to {end_date}")

    try:
        market_share_changes = await category_share_repo.get_category_market_share_changes(start_date=start_date, end_date=end_date)
        loguru.logger.info("Found market share changes!")
    except Exception as e:
        loguru.logger.error(f"Error retrieving market share changes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving market share changes"
        )

    changes = [
        CategoryMarketShareChange(
            category_id=entry['category_id'],
            market_share_change=entry['market_share_change']
        )
        for entry in market_share_changes
    ]

    return CategoryMarketShareChangeResponse(changes=changes)
