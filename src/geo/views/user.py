from geo.models import schemas
from geo.views import BaseView


class UserResponse(BaseView):
    content: schemas.users.UserModel