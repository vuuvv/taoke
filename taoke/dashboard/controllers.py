from taoke.dashboard.controller import Controller
from taoke.dashboard.models import DashboardMenu
from taoke.dashboard.sites import site

class DashboardMenuController(Controller):
    model = DashboardMenu

site.register(DashboardMenuController)

