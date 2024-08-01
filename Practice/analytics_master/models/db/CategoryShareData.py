import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from repository.tables import Base
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column


class CategoryShareData(Base):
    __tablename__ = 'category_share_data'

    date: Mapped[date] = mapped_column(sqlalchemy.Date, nullable=False)
    product_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category_details.category_id'), primary_key=True)
    market_share: SQLAlchemyMapped[float] = sqlalchemy_mapped_column(nullable=False)
