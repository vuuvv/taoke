from django.db import models
from django.utils.translation import ugettext_lazy as _

class OAuth(models.Model):
    code = models.CharField(_('Code'), maxlength=63)
    name = models.CharField(_('Name'), maxlength=63)
    app_key = models.CharField(_('App Key'), maxlength=255)
    app_secret = models.CharField(_('App Secret'), maxlength=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    auth = models.CharField(_('Author'), maxlength=63)
    ordering = models.IntegerField(_('Author'), default=1000)
    active = models.Boolean(_('Active'), default=True)

    class Meta:
        verbose_name = _('OAuth')
        verbose_name_plural = _('OAuth')
        ordering = ('ordering',)

    def __unicode__(self):
        return u'%s' % self.name

