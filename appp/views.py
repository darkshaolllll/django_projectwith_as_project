import os
from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view
from management.models import customer_information

@api_view(['POST'])
def handle_apk_request(request):
    """
    接收前端 JSON 数据，处理请求，返回对应名称的 APK 文件。
    :param request: HTTP 请求对象
    :return: 返回 APK 文件或错误信息
    """
    try:
        print("Received request: ", request.data)  # 一次性读取请求数据
        # 1. 获取前端发送的 JSON 数据，特别是 'name' 字段
        data = request.data  # 已经读取了 request.data，此时不再重新读取

        name = data.get('name')
        mac = data.get('mac')
        print("Name extracted from request: ", name)

        if not name:
            print("Name field is required but not provided")
            return JsonResponse({"detail": "Name field is required."}, status=400)

        # 2. 在 media 目录下查找对应的 APK 文件
        apk_file_path = find_apk_file_by_name(name)
        print("APK file path found: ", apk_file_path)

        if not apk_file_path:
            print("APK file not found for name: ", name)
            return JsonResponse({"detail": "APK file not found."}, status=404)

        # 3. 返回找到的 APK 文件
        print("Returning APK file for name: ", name)
        for key in mac:
            mac_selection = customer_information.objects.filter(mac=key.mac)
            mac_selection.name.update(name)
            mac_selection.save()
        return FileResponse(open(apk_file_path, 'rb'), content_type='application/vnd.android.package-archive')

    except Exception as e:
        print("Error processing request: ", str(e))
        return JsonResponse({"detail": str(e)}, status=500)

def find_apk_file_by_name(name):
    """
    根据文件名查找 media 目录中的 APK 文件
    :param name: APK 文件的名称（不含扩展名）
    :return: APK 文件的完整路径，若未找到则返回 None
    """
    # 获取 media 目录路径（需要确保 settings.py 中配置了 MEDIA_ROOT）
    media_dir = settings.MEDIA_ROOT
    print("Media directory: ", media_dir)

    # 拼接文件路径，查找名为 `<name>.apk` 的文件
    apk_file_path = os.path.join(media_dir, 'apk', f'{name}.apk')
    print("Constructed APK file path: ", apk_file_path)

    if os.path.exists(apk_file_path):
        print("APK file exists: ", apk_file_path)
        return apk_file_path
    else:
        print("APK file does not exist: ", apk_file_path)
        return None
