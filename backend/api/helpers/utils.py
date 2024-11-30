# pylint: disable=E0401
"""Utils."""

from typing import List
from uuid import UUID

import aiohttp
from api.schemas.auth import pwd_context

from core.config import MAX_IDS_EXIST
from core.constant import RECOMMENDATION_SERVICE_HOST
if MAX_IDS_EXIST:
    from core.config import map_track_ids


def get_password_hash(password: str) -> str:
    """Password to hash password"""
    return pwd_context.hash(password)


def get_tags_keywords(tags: List[str]) -> List[str]:
    """Get tags keywords."""
    return [tag.strip() for tag in tags]


async def get_recommendation(track_id: UUID, existed_ids: List[UUID]):
    """Get recommendation."""
    url = f"{RECOMMENDATION_SERVICE_HOST}/api/recommend"
    existed_ids = [str(existed_id) for existed_id in existed_ids]
    body = {"track_id": str(track_id), "existed_ids": existed_ids}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as response:
            res = await response.json(content_type=None)
            return [key for key, value in map_track_ids.items() if value in res['recommend_ids']]
