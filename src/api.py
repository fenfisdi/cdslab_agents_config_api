from os import environ

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from src.config import fastApiConfig
from src.db import MongoEngine
from src.routes import (
    disease_states_routes,
    distributions_routes,
    units_routes,
    configuration_routes,
    age_group_routes,
    natural_history_routes
)

app = FastAPI(**fastApiConfig)
db = MongoEngine().get_connection()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=environ.get("ALLOWED_HOSTS", "*").split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=environ.get("ALLOWED_METHODS", "*").split(","),
    allow_headers=environ.get("ALLOWED_HEADERS", "*").split(",")
)

app.include_router(units_routes)
app.include_router(distributions_routes)
app.include_router(disease_states_routes)
app.include_router(configuration_routes)
app.include_router(age_group_routes)
app.include_router(natural_history_routes)
