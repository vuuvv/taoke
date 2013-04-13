from taoke.dashboard.controller import Controller
from taoke.dashboard.models import Menu
from taoke.dashboard.sites import site

class DashboardMenuController(Controller):
    model = Menu

site.register(DashboardMenuController)

