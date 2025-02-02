# management/models.py

import re
from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from appp.models import apk_information


class channel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_("编号"))
    channel = models.CharField(max_length=100, unique=True, verbose_name=_("频道名称"))


    def __str__(self):
        return self.channel

    class Meta:
        verbose_name = _("频道")
        verbose_name_plural = _("频道")



class customer_information(models.Model):
    mac = models.CharField(max_length=100, unique=True, verbose_name=_("MAC地址"))  # MAC（唯一）
    app = models.JSONField(verbose_name=_("应用"))  # 应用，存储应用名称的列表
    channel = models.ForeignKey(channel, on_delete=models.CASCADE, verbose_name=_("频道"))

    def __str__(self):
        return f'MAC: {self.mac}, App: {self.app}'

    def clean(self):
        # 校验 mac 地址格式
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', self.mac):
            raise ValidationError(_('不是mac地址'))

        # 校验 app 字段的列表格式
        if not isinstance(self.app, list) or not all(isinstance(item, str) for item in this.app):
            raise ValidationError(_('每一个应用名称必须是字符串'))

    class Meta:
        verbose_name = _("客户信息")
        verbose_name_plural = _("客户信息")

    



def create_custom_permissions():
    content_type = ContentType.objects.get_for_model(channel)
    Permission.objects.get_or_create(
        codename='can_view_channel_entries',
        name=_('Can view channel entries'),
        content_type=content_type,
    )
