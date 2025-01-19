# management/models.py

import re
from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class channel(models.Model):
    id = models.AutoField(primary_key=True)
    channel = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 一对一外键到 User 模型

    def __str__(self):
        return self.channel

class user_information(models.Model):
    channel = models.ForeignKey(channel, on_delete=models.CASCADE)  # 外键到 Channel 表
    mac = models.CharField(max_length=100, unique=True)  # MAC（唯一）
    app = models.JSONField()  # 应用，二维数组
    wallpaper = models.BooleanField(default=False)  # 是否自定义壁纸
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # 数据的所有者

    def __str__(self):
        return f'Channel: {self.channel}, MAC: {self.mac}, App: {self.app}, Wallpaper: {self.wallpaper}, Owner: {self.owner}'

    def clean(self):
        # 校验 mac 地址格式
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', self.mac):
            raise ValidationError('不是mac地址')

        # 校验 app 字段的二维数组格式
        if not isinstance(self.app, list) or not all(isinstance(item, list) and len(item) == 2 for item in self.app):
            raise ValidationError('每一个变量必须含有两个元素')

        # 校验 app 字段中的每个元素
        for item in self.app:
            package_name, is_custom_icon = item
            if not isinstance(package_name, str) or not isinstance(is_custom_icon, bool):
                raise ValidationError('必须是bool类型')

# def create_custom_permissions():
#     content_type = ContentType.objects.get_for_model(channel)
#     permission = Permission.objects.create(
#         codename='can_view_channel_entries',
#         name='Can view channel entries',
#         content_type=content_type,
#     )
#     # 你可以在这里将权限分配给特定用户或组
#     user = User.objects.get(username='username')
#     user.user_permissions.add(permission)
