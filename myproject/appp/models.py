from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
class apk_information(models.Model):
    id = models.AutoField(primary_key=True)  # id 字段是自动递增的主键
    name = models.CharField(max_length=100, unique=True, db_index=True)  # name 字段是字符串，最大长度255，并设置为唯一索引
    version = models.FloatField(null=True, blank=True)  # version 字段是浮动数值类型，可为空

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # 为 name 字段创建索引
        ]


class requestion_information(models.Model):
    id = models.AutoField(primary_key=True)  # id 字段是自动递增的主键
    name = models.ForeignKey(apk_information, on_delete=models.CASCADE)  # name 字段是外键，引用 apk_information 的 name
    time = models.DateTimeField(auto_now_add=True)  # time 字段是日期时间类型，自动设置为当前时间
    ip = models.GenericIPAddressField()  # ip 字段是 IP 地址类型

    def __str__(self):
        return f"{self.name.name} - {self.ip} at {self.time}"



