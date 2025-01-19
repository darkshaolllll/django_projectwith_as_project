import os
import re
from pathlib import Path
from .models import apk_information
#正则表达式还需要完善
def process_apk_files(media_path):
    """
    自动识别 media 文件夹下的 APK 文件，提取信息并存储到 apk_information 表中。

    :param media_path: media 文件夹的路径
    """
    print(f"Starting process_apk_files with media_path: {media_path}")

    # 确保提供的路径有效
    if not os.path.exists(media_path):
        raise ValueError(f"The provided path {media_path} does not exist.")
    print(f"Valid media path: {media_path}")

    # 匹配 APK 文件的正则表达式，提取名称
    apk_pattern = re.compile(r"(.+)\.apk$", re.IGNORECASE)
    print("APK pattern compiled successfully")

    # 遍历 media 文件夹及其子目录
    for root, _, files in os.walk(media_path):
        print(f"Walking through directory: {root}")
        for file_name in files:
            if file_name.endswith('.apk'):
                file_path = Path(root) / file_name
                print(f"Processing file: {file_path}")

                # 提取文件名中的信息
                match = apk_pattern.match(file_name)
                if match:
                    name = match.group(1)
                    version = None  # 文件名中没有版本信息，因此设置为 None
                    print(f"Matched APK: {name}, Version: {version}")

                    # 检查是否已存在具有相同名称的记录
                    apk_obj, created = apk_information.objects.get_or_create(
                        name=name,
                        defaults={
                            'version': version
                        }
                    )

                    # 如果记录已存在但版本不同，则更新版本
                    if not created and apk_obj.version != version:
                        apk_obj.version = version
                        apk_obj.save()
                        print(f"Updated APK: {name}, Version: {version}")
                    else:
                        print(f"Created APK: {name}, Version: {version}")
                else:
                    print(f"Filename {file_name} did not match pattern")

    print("Finished processing APK files")
