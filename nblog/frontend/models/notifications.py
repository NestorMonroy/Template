from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class NotificationSetting(models.Model):
    CHANNELS = (
        ('mail', _('E-mail')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='notification_settings')
    action_type = models.CharField(max_length=255)
    # event = models.ForeignKey('Event', null=True, blank=True, on_delete=models.CASCADE,
    #                           related_name='notification_settings')
    method = models.CharField(max_length=255, choices=CHANNELS)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'action_type', 'method')
