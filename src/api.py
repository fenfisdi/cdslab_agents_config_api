from fastapi import FastAPI

from src.config import fastApiConfig
from src.db import MongoEngine
from src.routes import (
    units_routes, 
    distributions_routes,
    disease_states_routes
)

app = FastAPI(**fastApiConfig)
db = MongoEngine().get_connection()

app.include_router(units_routes)
app.include_router(distributions_routes)
app.include_router(disease_states_routes)
