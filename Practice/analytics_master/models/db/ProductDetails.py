import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from repository.tables import Base


class ProductDetails(Base):
    __tablename__ = 'product_details'

    #id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(autoincrement="auto")
    product_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, nullable=False)
    product_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=1024), nullable=False)
    brand_id = Column(Integer, ForeignKey('brand_data.brand_id'), nullable=False)