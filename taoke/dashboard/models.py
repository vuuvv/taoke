from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from mptt.models import MPTTModel, TreeForeignKey

class DashboardMenu(MPTTModel):
    name = models.CharField(_('Name'), max_length=255)
    data = models.CharField(_('Data'), max_length=255)
    memo = models.CharField(_('Memo'), max_length=255)
    favorite = models.BooleanField(_('Favorite'), default=False)
    visible = models.BooleanField(_('Visible'), default=True)

    parent = TreeForeignKey('self', null=True, blank=True, verbose_name=_('Parent'), related_name='children')
    groups = models.ManyToManyField(Group, blank=True, verbose_name=_('Group'), related_name='dashboard_menus')

    class Meta:
        verbose_name = _('Dashboard Menu')
        verbose_name_plural = _('Dashboard Menus')
        ordering = ('tree_id', 'lft')

    def __unicode__(self):
        return "%s" % self.name

