from geo.models import schemas
from geo.views import BaseView


class AccessTokenResponse(BaseView):
    content: schemas.token.AccessToken