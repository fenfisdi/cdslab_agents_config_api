from os import environ

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import PlainTextResponse

from src.config import fastApiConfig
from src.db import MongoEngine
from src.routes import (
    age_group_routes,
    configuration_routes,
    disease_states_routes,
    distributions_routes,
    execution_routes,
    immunization_routes,
    mobility_group_routes,
    natural_history_routes,
    population_routes,
    quarantine_group_routes,
    susceptibility_groups_routes,
    units_routes,
    vulnerability_group_routes
)
from src.services import ErrorAPI

app = FastAPI(**fastApiConfig)
db = MongoEngine().get_connection()


@app.exception_handler(Exception)
def http_error_report(_, exc: Exception):
    ErrorAPI.report_error(str(exc), code=500)
    return PlainTextResponse("Internal Server Error", status_code=500)


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
app.include_router(configuration_routes)
app.include_router(age_group_routes)
app.include_router(mobility_group_routes)
app.include_router(susceptibility_groups_routes)
app.include_router(immunization_routes)
app.include_router(vulnerability_group_routes)
app.include_router(disease_states_routes)
app.include_router(natural_history_routes)
app.include_router(quarantine_group_routes)
app.include_router(population_routes)
app.include_router(execution_routes)
