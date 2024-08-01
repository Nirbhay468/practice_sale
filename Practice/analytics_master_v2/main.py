import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from api.routers.SalesRouter import router as sales_router
from api.routers.CategoryRouter import router as category_router
from config.event import execute_backend_server_event_handler, terminate_backend_server_event_handler
from utils.LoadCsv import load_csv_to_db


def create_app() -> FastAPI:

    app = FastAPI()
    app.include_router(sales_router, prefix="/api")
    app.include_router(category_router, prefix="/api")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add event handlers
    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    return app


app = create_app()


@app.get("/load")
async def load_data():
    try:
        load_csv_to_db()
        logger.info("CSV loaded successfully.")
        return {"message": "CSV loaded successfully"}
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise fastapi.HTTPException(status_code=500, detail="Error loading CSV")

# @app.on_event("startup")
# def on_startup():
#     load_csv_to_db()
