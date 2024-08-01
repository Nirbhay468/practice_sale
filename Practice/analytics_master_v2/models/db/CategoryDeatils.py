import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from repository.tables import Base


class CategoryDetails(Base):
    __tablename__ = 'category_details'

    # id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(autoincrement="auto")
    category_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, nullable=False)
    category_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=1024), nullable=False)