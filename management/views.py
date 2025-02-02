from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from management.models import channel, customer_information

@api_view(['POST'])
@csrf_exempt
def first_requestion(request):
    if request.method == 'POST':
        try:
            print("收到数据", request.data)
            app = request.data.get('app')
            mac = request.data.get('mac')
            
            if not app or not mac:
                return Response({"error": "缺少app或mac参数"}, status=400)
            
            mac_selection = customer_information.objects.filter(mac=mac).first()  # 获取第一个匹配的对象
            print(mac_selection)
            if mac_selection is None:
                if app is not None:
                    print(app)
                    
                    # 获取或创建一个固定的 channel 实例
                    fixed_channel, created = channel.objects.get_or_create(channel="固定频道名称")
                    
                    new_customer = customer_information(mac=mac, app=app, channel=fixed_channel)
                    new_customer.save()
                    return Response({"message": "successful"})
                else:
                    return Response({"error": "应用不存在"}, status=404)
            else:
                return Response({"error": f"{mac_selection} 该用户已存在"}, status=400)
            
        except Exception as e:
            print("发生错误：", str(e))
            return Response({"error": f"发生错误: {str(e)}"}, status=500)
    else:
        return Response({"error": "仅支持POST请求"}, status=405)
