from taoke.dashboard.controller import Controller
from taoke.dashboard.models import Menu
from taoke.dashboard.sites import site

from django.contrib.auth.models import User

class DashboardMenuController(Controller):
    model = Menu
    fields = ('name', 'data', 'memo', 'visible', 'favorite')

site.register(DashboardMenuController)

class UserController(Controller):
    model = User
    list_display = ('username', 'last_login')

site.register(UserController)

