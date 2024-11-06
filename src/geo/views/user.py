from geo.models import schemas
from geo.views import BaseView

class UserLoginResponse(BaseView):
    content: schemas.users.UserLoginModel

class UserRegisterResponse(BaseView):
    content: schemas.users.UserRegisterModel