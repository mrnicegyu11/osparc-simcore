import logging

from aiohttp import web
from aiohttp.web import RouteTableDef
from models_library.api_schemas_webserver.auth import ApiKeyCreate
from servicelib.aiohttp import status
from servicelib.aiohttp.requests_validation import parse_request_body_as
from servicelib.mimetype_constants import MIMETYPE_APPLICATION_JSON
from simcore_postgres_database.errors import DatabaseError

from .._meta import API_VTAG
from ..login.decorators import login_required
from ..models import RequestContext
from ..security.decorators import permission_required
from ..utils_aiohttp import envelope_json_response
from . import _api

_logger = logging.getLogger(__name__)


routes = RouteTableDef()


@routes.get(f"/{API_VTAG}/auth/api-keys", name="list_api_keys")
@login_required
@permission_required("user.apikey.*")
async def list_api_keys(request: web.Request):
    req_ctx = RequestContext.model_validate(request)
    api_keys_names = await _api.list_api_keys(
        request.app,
        user_id=req_ctx.user_id,
        product_name=req_ctx.product_name,
    )
    return envelope_json_response(api_keys_names)


@routes.post(f"/{API_VTAG}/auth/api-keys", name="create_api_key")
@login_required
@permission_required("user.apikey.*")
async def create_api_key(request: web.Request):
    req_ctx = RequestContext.model_validate(request)
    new = await parse_request_body_as(ApiKeyCreate, request)
    try:
        data = await _api.create_api_key(
            request.app,
            new=new,
            user_id=req_ctx.user_id,
            product_name=req_ctx.product_name,
        )
    except DatabaseError as err:
        raise web.HTTPBadRequest(
            reason="Invalid API key name: already exists",
            content_type=MIMETYPE_APPLICATION_JSON,
        ) from err

    return envelope_json_response(data)


@routes.delete(f"/{API_VTAG}/auth/api-keys", name="delete_api_key")
@login_required
@permission_required("user.apikey.*")
async def delete_api_key(request: web.Request):
    req_ctx = RequestContext.model_validate(request)

    # NOTE: SEE https://github.com/ITISFoundation/osparc-simcore/issues/4920
    body = await request.json()
    name = body.get("display_name")

    try:
        await _api.delete_api_key(
            request.app,
            name=name,
            user_id=req_ctx.user_id,
            product_name=req_ctx.product_name,
        )
    except DatabaseError as err:
        _logger.warning(
            "Failed to delete API key %s. Ignoring error", name, exc_info=err
        )

    return web.json_response(status=status.HTTP_204_NO_CONTENT)
