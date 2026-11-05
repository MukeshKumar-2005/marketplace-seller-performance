from fastapi import FastAPI

from api.routes.analytics import router


app = FastAPI(
    title="Marketplace Seller Performance API",
    description="API for seller performance analytics",
    version="1.0.0"
)


app.include_router(router, prefix="/api")


@app.get("/")
def home():

    return {
        "message": "Marketplace Seller Performance API is running!"
    }