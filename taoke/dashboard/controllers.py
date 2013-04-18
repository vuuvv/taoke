from taoke.dashboard.controller import Controller
from taoke.dashboard.models import Menu
from taoke.dashboard.sites import site

from django.contrib.auth.models import User, Group

class DashboardMenuController(Controller):
    model = Menu
    fields = ('parent', 'name', 'view', 'data', 'memo', 'visible', 'favorite')
    list_display = ('name', 'view', 'visible', 'favorite')

site.register(DashboardMenuController)

class UserController(Controller):
    model = User
    list_display = ('username', 'last_login')
    fields = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')

site.register(UserController)

class GroupController(Controller):
    model = Group
    list_display = ('name', )
    fields = ('name', )

