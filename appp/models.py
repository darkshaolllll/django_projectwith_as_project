from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

class apk_information(models.Model):  # APK信息
    id = models.AutoField(primary_key=True, verbose_name=_("编号"))  # 编号，自动递增主键
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name=_("名称"))  # 名称，最大长度100，唯一索引
    packagename=models.CharField(max_length=100,unique=True,verbose_name=("包名"))
    version = models.FloatField(null=True, blank=True, verbose_name=_("版本号"))  # 版本号，可为空

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='name_idx'),  # 为名称创建索引
        ]
        verbose_name = _("APK信息")
        verbose_name_plural = _("APK信息")


class requestion_information(models.Model):  # 请求信息
    id = models.AutoField(primary_key=True, verbose_name=_("编号"))  # 编号，自动递增主键
    name = models.ForeignKey(apk_information, verbose_name=_("APK信息"), on_delete=models.CASCADE)  # APK名称，外键引用apk_information
    time = models.DateTimeField(auto_now_add=True, verbose_name=_("请求时间"))  # 请求时间，自动设置为当前时间
    ip = models.GenericIPAddressField(verbose_name=_("IP地址"))  # IP地址

    def __str__(self):
        return f"{self.name.name} - {self.ip} at {self.time}"

    class Meta:
        verbose_name = _("请求信息")
        verbose_name_plural = _("请求信息")


