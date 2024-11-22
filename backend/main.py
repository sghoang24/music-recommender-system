# pylint: disable=E0401
"""Application for backend service."""

# import aioredis # Not use for ubuntu
import redis.asyncio as redis  # Use for Ubuntu
import uvicorn
from api.database.models import db
from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from api.routes.api import app as api_router
from api.services.user_service import UserService
from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from core.constant import APP_HOST, APP_PORT, REDIS_HOST, REDIS_PORT
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_limiter import FastAPILimiter
from logger.logger import custom_logger
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse


def get_application() -> FastAPI:
    """Get app."""

    async def lifespan(app: FastAPI):
        """Start up application."""
        # Create admin user
        user_service = UserService()
        user_service.create_user_admin(db.SessionLocal())

        redis_host = REDIS_HOST if REDIS_HOST else "localhost"
        redis_port = REDIS_PORT if REDIS_PORT else 6379
        custom_logger.info(f"Redis DB URL: redis://{redis_host}:{redis_port}")
        redis_connection = redis.from_url(f"redis://{redis_host}:{redis_port}", encoding="utf8")  # For Ubuntu
        await FastAPILimiter.init(redis_connection)
        FastAPICache.init(InMemoryBackend())

        yield  # Signals that startup is complete

        custom_logger.info("Shutting down application...")
        await redis_connection.close()

    application = FastAPI(
        lifespan=lifespan,
        title=PROJECT_NAME,
        debug=DEBUG,
        version=VERSION,
        docs_url=None,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router, prefix=API_PREFIX)

    application.mount("/static", StaticFiles(directory="fe/static"), name="static")

    @application.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html(
        # current_user: UserSchema = Depends(authentication_service.get_current_active_user)
    ):
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
        with open("../logs/backend/backend.log", "r", encoding="utf-8") as f:
            log_str = f.read()
            log_html = f"<pre>{log_str}</pre>"
            return log_html

    @application.get("/")
    async def web_app() -> HTMLResponse:
        """Web App."""
        custom_logger.info("Welcome to Back-End Service")
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
