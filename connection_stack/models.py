import re
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class requestion_of_ali(models.Model):
    id=models.AutoField(primary_key=True,verbose_name=("编号"))
    mac = models.CharField(max_length=100, unique=True, verbose_name=_("MAC地址"))
    app = models.JSONField(verbose_name=_("应用"))
    def __str__(self):
        return f'MAC: {self.mac}, App: {self.app}'

    def clean(self):
        # 校验 mac 地址格式
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', self.mac):
            raise ValidationError(_('不是mac地址'))


    class Meta:
        verbose_name = _("ali服务器信息")
        verbose_name_plural = _("ali服务器信息")
