from fastapi import FastAPI
from repository.database import async_db
import fastapi
import loguru
from sqlalchemy.ext.asyncio import AsyncConnection
from models.db.BrandData import *
from models.db.ProductDetails import *
from models.db.SalesData import *
from models.db.CategoryShareData import *
from models.db.ProductCategoryMapping import *
from models.db.CategoryDeatils import *


async def initialize_db_tables(connection: AsyncConnection) -> None:
    loguru.logger.info("Database Table Creation --- Initializing . . .")

    await connection.run_sync(Base.metadata.drop_all)
    await connection.run_sync(Base.metadata.create_all)

    loguru.logger.info("Database Table Creation --- Successfully Initialized!")


async def initialize_db_connection(backend_app: FastAPI) -> None:
    try:
        loguru.logger.info("Database Connection --- Establishing . . .")

        backend_app.state.db = async_db

        async with backend_app.state.db.async_engine.begin() as connection:
            await initialize_db_tables(connection=connection)

        loguru.logger.info("Database Connection --- Successfully Established!")

    except Exception as e:
        loguru.logger.error(f"Database Connection --- Failed to Establish: {e}")


async def dispose_db_connection(backend_app: fastapi.FastAPI) -> None:
    loguru.logger.info("Database Connection --- Disposing . . .")

    await backend_app.state.db.async_engine.dispose()

    loguru.logger.info("Database Connection --- Successfully Disposed!")
