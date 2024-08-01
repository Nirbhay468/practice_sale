from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from models.schemas.base import BaseSchemaModel


class SalesResponse(BaseSchemaModel):
    transaction_id: int
    quantity: int
    revenue: float
    product: int
    date: date


class SalesSummary(BaseModel):
    product: int
    total_quantity: int
    total_revenue: float


class SalesResponseList(BaseModel):
    summery: List[SalesSummary]
    sales: List[SalesResponse]


class SaleSummary(BaseModel):
    total_quantity: int
    total_revenue: float
    start_date: Optional[str]
    end_date: Optional[str]


class TotalSalesResponse(BaseModel):
    sale: List[SaleSummary]


class SaleSummaryByDimensions(BaseModel):
    category: Optional[int] = None
    brand: Optional[int] = None
    product: Optional[int] = None
    total_quantity: int
    total_revenue: float


class TotalSalesResponseByDimensions(BaseModel):
    sale: List[SaleSummaryByDimensions]
