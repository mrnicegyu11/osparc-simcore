from pydantic import PositiveInt
from pydantic.types import NonNegativeInt

UserID = PositiveInt
ClusterID = NonNegativeInt

# dynamic services
DYNAMIC_SIDECAR_SERVICE_PREFIX = "dy-sidecar"
DYNAMIC_PROXY_SERVICE_PREFIX = "dy-proxy"

REGEX_DY_SERVICE_SIDECAR = fr"^{DYNAMIC_SIDECAR_SERVICE_PREFIX}_[a-zA-Z0-9-_]*"
REGEX_DY_SERVICE_PROXY = fr"^{DYNAMIC_PROXY_SERVICE_PREFIX}_[a-zA-Z0-9-_]*"
