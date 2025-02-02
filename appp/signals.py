import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import apk_information
from .utils import process_apk_files  # 导入 process_apk_files 函数


@receiver(post_migrate)
def run_process_apk_files(sender, **kwargs):
    media_path = "E:/代码/djangostudy/myproject/media/apk"  # 使用实际存在的路径
    if os.path.exists(media_path):
        process_apk_files(media_path)
        print("Processed APK files after migration")
    else:
        print(f"The provided path {media_path} does not exist.")
