import loguru
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import date, timedelta
from typing import Optional, List
from api.dependencies.repository import get_repository
from models.schemas.SalesResponse import SalesResponse, SalesResponseList, SalesSummary, TotalSalesResponse, \
    SaleSummary, TotalSalesResponseByDimensions, SaleSummaryByDimensions
from repository.crud.productDetails import ProductDetailCRUDRepository
from repository.crud.sales import SalesCRUDRepository
from utils.exceptions.database import EntityDoesNotExist
from utils.exceptions.http.exc_4xx import http_404_exc_id_not_found_request

router = APIRouter()


@router.get(
    path="/totalSale",
    name="sales:read-total-sales",
    response_model=TotalSalesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_total_sales(
        start_date: Optional[date] = Query(None, description="Start date for the sales period"),
        end_date: Optional[date] = Query(None, description="End date for the sales period"),
        sales_repo: SalesCRUDRepository = Depends(get_repository(repo_type=SalesCRUDRepository))
) -> TotalSalesResponse:
    loguru.logger.info(f"Received request from {start_date} to {end_date}")

    # Handle date validation and defaulting
    if (start_date and not end_date) or (not start_date and end_date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both start_date and end_date must be provided together or neither should be provided."
        )

    # Default to one week of data if both dates are None
    if not start_date and not end_date:
        end_date = date.today()
        start_date = end_date - timedelta(weeks=1)

    # Validate date range
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date"
        )

    try:
        # Fetch sales data for the specified date range
        sales_summary = await sales_repo.get_sales_by_and_date_range(
            start_date=start_date,
            end_date=end_date
        )
        loguru.logger.info("Found sales data!")
    except EntityDoesNotExist:
        loguru.logger.error("No sales data found for the specified date range")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sales data found for the specified date range"
        )

    # Create the response list
    sale_summaries = []
    for entry in sales_summary:
        sale_summaries.append(
            SaleSummary(
                total_quantity=entry.total_quantity,
                total_revenue=entry.total_revenue,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat()
            )
        )

    return TotalSalesResponse(sale=sale_summaries)


@router.get(
    "/sales-by-dimensions",
    name="sales:read-total-sales",
    response_model=TotalSalesResponseByDimensions,
    status_code=status.HTTP_200_OK,
)
async def get_total_sales_by_dimensions(
        group_by: Optional[List[str]] = Query(None, description="Fields to group by, e.g., 'product'"),
        sales_repo: SalesCRUDRepository = Depends(get_repository(repo_type=SalesCRUDRepository))
) -> TotalSalesResponseByDimensions:
    loguru.logger.info(f"Received request with group_by fields: {group_by}")

    try:
        # Fetch sales data for the specified grouping
        sales_summary = await sales_repo.get_sales_by_fields(group_by_fields=group_by)
        loguru.logger.info("Found sales data!")
    except Exception as e:
        loguru.logger.error(f"Error retrieving sales data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving sales data"
        )

    sale_summaries = []
    for entry in sales_summary:
        sale_summary_data = {
            'total_quantity': entry['total_quantity'],
            'total_revenue': entry['total_revenue']
        }
        for field in group_by:
            if entry.get(field) is not None:
                sale_summary_data[field] = entry[field]

        sale_summaries.append(SaleSummaryByDimensions(**sale_summary_data))

    return TotalSalesResponseByDimensions(sale=sale_summaries)


@router.get(
    path="/sale/brand/{brand_id}",
    name="sales:read-sales-by-brand_id",
    response_model=SalesResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_sales_by_brand_id(
        brand_id: int,
        product_detail_repo: ProductDetailCRUDRepository = Depends(
            get_repository(repo_type=ProductDetailCRUDRepository)),
        sales_repo: SalesCRUDRepository = Depends(get_repository(repo_type=SalesCRUDRepository))
) -> SalesResponseList:
    loguru.logger.info(f"Received request for brand_id: {brand_id}")

    try:
        db_product_detail = await product_detail_repo.get_product_by_brand_id(brand_id=brand_id)
        product_ids = [product_detail.product_id for product_detail in db_product_detail]
        db_sales = await sales_repo.get_sales_by_product_ids(product_ids=product_ids)
        loguru.logger.info("Found sales data!")
    except EntityDoesNotExist:
        loguru.logger.error(f"Transaction ID {brand_id} does not exist")
        raise await http_404_exc_id_not_found_request(id=brand_id)

    loguru.logger.info(f"Returning sales data for transaction_id: {brand_id}")

    # Group sales by product
    sales_by_product = {}
    for sale in db_sales:
        product_id = sale.product
        if product_id not in sales_by_product:
            sales_by_product[product_id] = {
                'total_quantity': 0,
                'total_revenue': 0.0,
                'sales': []
            }

        sales_by_product[product_id]['total_quantity'] += sale.quantity
        sales_by_product[product_id]['total_revenue'] += sale.revenue
        sales_by_product[product_id]['sales'].append(
            SalesResponse(
                transaction_id=sale.transaction_id,
                quantity=sale.quantity,
                revenue=sale.revenue,
                product=product_id,
                date=sale.date
            )
        )

    # Create the response list
    sales_responses = []
    sales_summaries = []
    for product_id, data in sales_by_product.items():
        sales_responses.extend(data['sales'])
        sales_summaries.append(
            SalesSummary(
                product=product_id,
                total_quantity=data['total_quantity'],
                total_revenue=data['total_revenue'],
            )
        )

    return SalesResponseList(summery=sales_summaries,sales=sales_responses)


@router.get(
    path="/sales/{transaction_id}",
    name="sales:read-sales-by-transaction_id",
    response_model=SalesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_sales_by_transaction_id(
        transaction_id: int,
        sales_repo: SalesCRUDRepository = Depends(get_repository(repo_type=SalesCRUDRepository)),
) -> SalesResponse:
    loguru.logger.info(f"Received request for transaction_id: {transaction_id}")
    try:
        db_sales = await sales_repo.get_sales_by_transaction_id(transaction_id=transaction_id)
        loguru.logger.info("Found sales data!")
    except EntityDoesNotExist:
        loguru.logger.error(f"Transaction ID {transaction_id} does not exist")
        raise await http_404_exc_id_not_found_request(id=transaction_id)

    loguru.logger.info(f"Returning sales data for transaction_id: {transaction_id}")

    return SalesResponse(
        quantity=db_sales.quantity,
        revenue=db_sales.revenue,
        product=db_sales.product,
        transaction_id=db_sales.transaction_id,
        date=db_sales.date
    )