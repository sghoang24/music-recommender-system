# pylint: disable=E0401
"""Define API."""

from api.routes import recommend_route
from fastapi import APIRouter

app = APIRouter()

app.include_router(recommend_route.router, tags=["Recommendation"], prefix="/recommend")
