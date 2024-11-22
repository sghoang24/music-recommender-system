# pylint: disable=E0401
"""Recommendation route."""

from api.errors.error_message import BaseErrorMessage
from api.responses.base import BaseResponse
from api.schemas.recommend import RecommendInputSchema
from api.services.recommend import recommendation_service
from fastapi import APIRouter
from logger.logger import custom_logger

router = APIRouter()


@router.post("/", include_in_schema=True)
async def recommend(recommend_input: RecommendInputSchema):
    """Recommend."""
    try:
        recommend_res = recommendation_service.get_recommendation(
            track_id=recommend_input.track_id,
            existed_ids=recommend_input.existed_ids,
        )
        custom_logger.info("[recommendation] Recommend music succesful with track_ids = %s", recommend_input.track_id)
        return recommend_res

    except ValueError as e:
        error_object: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            message_code=error_object.message_code,
            message=error_object.message,
            status_code=error_object.status_code,
        )
    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message=f"An error occurred: {e}")
