# pylint: disable=E0401
"""Application for recommendation service."""

import uvicorn
from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from api.routes.api import app as api_router
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from core.constant import APP_HOST, APP_PORT
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from logger.logger import custom_logger
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse


def get_application() -> FastAPI:
    """Get app."""
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, docs_url=None)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router, prefix=API_PREFIX)
    application.mount("/static", StaticFiles(directory="fe/static"), name="static")

    @application.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        """Swagger UI."""
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/js/swagger-ui-bundle.js",
            swagger_css_url="/static/js/swagger-ui.css",
        )

    @application.get("/signin/{verify_token}", include_in_schema=False)
    async def custom_ui_signin(verify_token: str):
        """Callback for UI signin."""
        return get_swagger_ui_html(
            openapi_url=application.openapi_url,
            title=application.title + " - Swagger UI",
            oauth2_redirect_url=application.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/js/swagger-ui-bundle.js",
            swagger_css_url="/static/js/swagger-ui.css",
        )

    @application.get(application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @application.get("/logger", response_class=HTMLResponse, include_in_schema=False)
    async def get_logger():
        """Get logger."""
        with open("../logs/recommendation/recommendation.log", "r", encoding="utf-8") as f:
            log_str = f.read()
            log_html = f"<pre>{log_str}</pre>"
            return log_html

    @application.get("/")
    async def web_app() -> HTMLResponse:
        """Web App."""
        custom_logger.info("Welcome to Recommendation Service")
        with open("fe/templates/index.html", encoding="utf-8") as f:
            html = f.read()
        return HTMLResponse(html)

    return application


async def app_handler(scope, receive, send):
    """App handler."""
    await app(scope, receive, send)


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=int(APP_PORT), reload=True)
