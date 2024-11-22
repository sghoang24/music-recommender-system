# pylint: disable=E0401
"""Base Response."""

from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, ORJSONResponse
from pydantic import BaseModel, Field
from starlette import status

DataResponseType = TypeVar("DataResponseType")


class HttpResponseSchema(BaseModel, Generic[DataResponseType]):
    """HTTP Response Schema."""

    message_code: int = Field(..., description="Numeric code indicating the type of message or response.")
    message: str = Field(..., description="Human-readable message providing additional context about the response.")
    data: Optional[DataResponseType] = Field(None, description="Optional data accompanying the response.")


class BaseResponse:
    """Base Response."""

    @staticmethod
    def success_response(
        message: str = "API success",
        status_code: int = status.HTTP_200_OK,
        message_code: int = 0,
        data=None,
    ):
        """Success response with a message and status code."""
        if data is None:
            return JSONResponse(
                status_code=status_code,
                content={
                    "message_code": message_code,
                    "message": message,
                },
            )
        else:
            return ORJSONResponse(
                status_code=status_code,
                content={
                    "message_code": message_code,
                    "message": message,
                    "data": jsonable_encoder(data),
                },
            )

    @staticmethod
    def error_response(
        message: str = "API error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message_code: int = 0,
    ):
        """Error response with a message and status code."""
        return JSONResponse(
            status_code=status_code,
            content={
                "message_code": message_code,
                "message": message,
            },
        )
