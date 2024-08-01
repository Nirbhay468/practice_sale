from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from repository.tables import Base


class ProductCategoryMapping(Base):
    __tablename__ = 'product_category_mapping'
    product_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category_details.category_id'), nullable=False)
