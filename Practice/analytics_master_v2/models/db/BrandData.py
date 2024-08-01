import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from repository.tables import Base

class Brand(Base):
    __tablename__ = 'brand_data'
    # id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(autoincrement="auto")
    brand_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True)
    brand_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=1024), nullable=False)
