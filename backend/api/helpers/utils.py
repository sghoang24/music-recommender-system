# pylint: disable=E0401
"""Utils."""

from typing import List
from uuid import UUID

import aiohttp
from api.schemas.auth import pwd_context
from core.constant import RECOMMENDATION_SERVICE_HOST


def get_password_hash(password: str) -> str:
    """Password to hash password"""
    return pwd_context.hash(password)


def get_tags_keywords(tags: List[str]) -> List[str]:
    """Get tags keywords."""
    return [tag.strip() for tag in tags]


async def get_recommendation(track_id: UUID, existed_ids: List[UUID]):
    """Get recommendation."""
    url = f"{RECOMMENDATION_SERVICE_HOST}/api/recommend"
    body = {"track_id": track_id, "existed_ids": existed_ids}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as response:
            res = await response.json(content_type=None)
            return res
