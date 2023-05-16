import logging

from fastapi import APIRouter, Depends, Security

from ...models.schemas.profiles import Profile, ProfileUpdate
from ...plugins.webserver import AuthSession
from ..dependencies.webserver import get_webserver_session

_logger = logging.getLogger(__name__)


router = APIRouter()
# SEE: https://www.python-httpx.org/async/
# TODO: path mapping and operation


@router.get("", response_model=Profile)
async def get_my_profile(
    client: AuthSession = Depends(get_webserver_session),
) -> Profile:
    data = await client.get("/me")
    profile = Profile.parse_obj(data)

    return profile


@router.put("", response_model=Profile)
async def update_my_profile(
    profile_update: ProfileUpdate,
    client: AuthSession = Security(get_webserver_session, scopes=["write"]),
) -> Profile:
    # FIXME: replace by patch
    # TODO: improve. from patch -> put, we need to ensure it has a default in place
    profile_update.first_name = profile_update.first_name or ""
    profile_update.last_name = profile_update.last_name or ""

    await client.put("/me", body=profile_update.dict())

    profile: Profile = await get_my_profile(client)
    return profile
