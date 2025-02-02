from sqlite3 import DatabaseError
from django.shortcuts import render

from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from management.models import customer_information
from appp.models import apk_information
import datetime
from .models import requestion_of_ali
from appp.views import find_apk_file_by_name
from rest_framework.decorators import api_view
from rest_framework.response import Response




key_word=[]
def arrange_variable(name, mac, key_word):
    getjson = {"name": name, "mac": mac, "time": datetime.datetime.now()}
    key_word.append(getjson)
    return key_word


@api_view(['POST'])
@csrf_exempt
def handle_ali_request(request):
    if request.method == 'POST':
        try:
            print("收到数据", request.data)
            name = request.data.get('name')
            mac = request.data.get('mac')
            
            if not name or not mac:
                return Response({"error": "缺少name或mac参数"}, status=400)
            
            mac_selection = customer_information.objects.filter(mac=mac).first()  # 获取第一个匹配的对象
            print(mac_selection)
            if mac_selection and isinstance(mac_selection.app, list) and name not in mac_selection.app:
                app_exists = apk_information.objects.filter(packagename=name).exists()
                if app_exists:
                    print("名字匹配并且应用存在")
                    exchange = arrange_variable(name, mac, key_word)
                    mac_json={}
                    for key in exchange:
                        if name:
                            mac_json = {"name": name}
                        else:
                            return JsonResponse({"error": "MAC 地址未提供"}, status=400)
                        
                        new_requestion = requestion_of_ali(mac=key['mac'], app=mac_json)
                        new_requestion.save()
                    return Response({"message": "successful"})
                else:
                    return Response({"error": "应用不存在"}, status=404)
            else:
                return Response({"error": f"{mac_selection}没有该用户或用户已下载该应用"}, status=400)
            
        except Exception as e:
            print("发生错误：", str(e))
            return Response({"error": f"发生错误: {str(e)}"}, status=500)
    else:
        return Response({"error": "仅支持POST请求"}, status=405)





@api_view(['POST'])
@csrf_exempt
def polling(request):
    if request.method == 'POST':
        try:
            # 读取一次数据
            box_mac = request.data.get('mac')
            if not box_mac:
                return Response({"error": "缺少 mac 参数"}, status=400)
            
            # 查询数据库
            mac_selection = requestion_of_ali.objects.filter(mac=box_mac).first()
            
            if mac_selection is not None:
                # 处理 APK 请求
                return handle_apk_request(request.data)
            else:
                print(f"{box_mac} 暂时没有找到相应记录")
                return Response({"error": f"{box_mac} 暂时没有找到相应记录"}, status=404)
                
        except KeyError:
            return Response({"error": "请求数据格式错误"}, status=400)
        except requestion_of_ali.DoesNotExist:
            return Response({"error": "数据库查询错误：未找到相应记录"}, status=404)
        except requestion_of_ali.MultipleObjectsReturned:
            return Response({"error": "数据库查询错误：返回了多个记录"}, status=500)
        except DatabaseError as e:
            print("数据库错误：", str(e))
            return Response({"error": f"数据库错误: {str(e)}"}, status=500)
        except Exception as e:
            print("发生错误：", str(e))
            return Response({"error": f"发生未知错误: {str(e)}"}, status=500)
    else:
        return Response({"error": "仅支持 POST 请求"}, status=405)

def handle_apk_request(data):
    """
    接收前端 JSON 数据，处理请求，返回对应名称的 APK 文件。
    :param data: 请求的数据（而非 request 对象）
    :return: 返回 APK 文件或错误信息
    """
    try:
        print("Received request: ", data)  # 直接使用传递的数据

        # 获取前端发送的 JSON 数据，特别是 'mac' 字段
        mac = data.get('mac')
        if not mac:
            print("mac 参数缺失")
            return JsonResponse({"detail": "mac 参数缺失"}, status=400)

        # 查询数据库获取对应的名称
        mac_selection = requestion_of_ali.objects.filter(mac=mac).first()
        if mac_selection is None:
            print(f"没有找到 mac 对应的记录: {mac}")
            return JsonResponse({"detail": f"没有找到 mac 对应的记录: {mac}"}, status=404)

        app = mac_selection.app
        print("Name extracted from request: ", app)

        # 在 media 目录下查找对应的 APK 文件
        apk_file_path = find_apk_file_by_name(app.get("name"))
        print("APK file path found: ", apk_file_path)

        if not apk_file_path:
            print("APK file not found for name: ", app)
            return JsonResponse({"detail": "APK file not found."}, status=404)

        # 返回找到的 APK 文件
        print("Returning APK file for name: ", app)

        # 删除对应的 `requestion_of_ali` 记录
        if mac:
            print(f"Deleting requestion_of_ali record with mac: {mac}")
            requestion_of_ali.objects.filter(mac=mac).delete()

        return FileResponse(open(apk_file_path, 'rb'), content_type='application/vnd.android.package-archive')

    except KeyError as e:
        print("KeyError: ", str(e))
        return JsonResponse({"detail": f"请求数据格式错误: {str(e)}"}, status=400)
    except requestion_of_ali.DoesNotExist:
        print("DoesNotExist: 数据库中没有找到对应记录")
        return JsonResponse({"detail": "数据库中没有找到对应记录"}, status=404)
    except requestion_of_ali.MultipleObjectsReturned:
        print("MultipleObjectsReturned: 数据库中返回了多个记录")
        return JsonResponse({"detail": "数据库中返回了多个记录"}, status=500)
    except FileNotFoundError:
        print("FileNotFoundError: 指定的 APK 文件未找到")
        return JsonResponse({"detail": "指定的 APK 文件未找到"}, status=404)
    except Exception as e:
        print("Error processing request: ", str(e))
        return JsonResponse({"detail": f"发生未知错误: {str(e)}"}, status=500)

