from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode

from mptt.models import MPTTModel, TreeForeignKey

class Menu(MPTTModel):
    name = models.CharField(_('Name'), max_length=255)
    data = models.CharField(_('Data'), blank=True, null=True, max_length=255)
    memo = models.CharField(_('Memo'), blank=True, null=True, max_length=255)
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

ADDITION = 1
CHANGE = 2
DELETION = 3

class LogEntryManager(models.Manager):
    def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
        e = self.model(None, None, user_id, content_type_id, smart_unicode(object_id), object_repr[:200], action_flag, change_message)
        e.save()

class LogEntry(models.Model):
    action_time = models.DateTimeField(_('action time'), auto_now=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(_('object id'), blank=True, null=True)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_('action flag'))
    change_message = models.TextField(_('change message'), blank=True)

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        db_table = 'django_admin_log'
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_unicode(self.action_time)

    def __unicode__(self):
        if self.action_flag == ADDITION:
            return _('Added "%(object)s".') % {'object': self.object_repr}
        elif self.action_flag == CHANGE:
            return _('Changed "%(object)s" - %(changes)s') % {'object': self.object_repr, 'changes': self.change_message}
        elif self.action_flag == DELETION:
            return _('Deleted "%(object)s."') % {'object': self.object_repr}

    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION

    def get_edited_object(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

