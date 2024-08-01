import sqlalchemy
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from repository.tables import Base


class SalesData(Base):
    __tablename__ = "sales_data"
    # id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(autoincrement="auto")
    transaction_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(sqlalchemy.Date, nullable=False)
    product = Column(Integer, ForeignKey('product_details.product_id'), nullable=False)
    quantity: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)
    revenue: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)