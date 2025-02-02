import os
import re
from pathlib import Path
from apkutils import APK  # 假设你已经使用了正确的 APK 解析库
from appp.models import apk_information

def get_apk_package_names(folder_path):
    package_names = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".apk"):
                apk_path = os.path.join(root, file)
                try:
                    apk = APK(apk_path)
                    package_names[file] = apk.manifest.package_name
                except Exception as e:
                    package_names[file] = f"解析失败: {e}"
    return package_names

def process_apk_files(media_path):
    print(f"Starting process_apk_files with media_path: {media_path}")

    if not os.path.exists(media_path):
        raise ValueError(f"The provided path {media_path} does not exist.")
    print(f"Valid media path: {media_path}")

    package_names = get_apk_package_names(media_path)
    print("APK package names retrieved successfully")

    apk_pattern = re.compile(r"(.+)\.apk$", re.IGNORECASE)
    print("APK pattern compiled successfully")

    for root, _, files in os.walk(media_path):
        print(f"Walking through directory: {root}")
        for file_name in files:
            if file_name.endswith('.apk'):
                file_path = Path(root) / file_name
                print(f"Processing file: {file_path}")

                match = apk_pattern.match(file_name)
                if match:
                    name = match.group(1)  # 从文件名中提取名称
                    version = None  # 默认版本号为 None
                    package_name = package_names.get(file_name, "未知包名")
                    print(f"Matched APK: {name}, Version: {version}, Package Name: {package_name}")

                    # 重命名文件为包名
                    new_file_name = f"{package_name}.apk"
                    new_file_path = Path(root) / new_file_name
                    if file_path != new_file_path:
                        os.rename(file_path, new_file_path)
                        print(f"Renamed {file_name} to {new_file_name}")

                    # 检查是否已有记录
                    apk_obj, created = apk_information.objects.get_or_create(
                        name=name,
                        defaults={
                            'version': version,
                            'packagename': package_name
                        }
                    )

                    if not created:  # 如果记录已存在
                        updated = False
                        if apk_obj.name != name:
                            apk_obj.name = name
                            updated = True
                        if apk_obj.packagename != package_name:
                            apk_obj.packagename = package_name
                            updated = True
                        if apk_obj.version != version:
                            apk_obj.version = version
                            updated = True
                        if updated:
                            apk_obj.save()
                            print(f"Updated APK: {name}, Version: {version}, Package Name: {package_name}")
                        else:
                            print(f"No changes for APK: {name}, Package Name: {package_name}")
                    else:
                        print(f"Created APK: {name}, Version: {version}, Package Name: {package_name}")
                else:
                    print(f"Filename {file_name} did not match pattern")

    print("Finished processing APK files")
