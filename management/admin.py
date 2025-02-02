from django.contrib import admin
from .models import channel, customer_information

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('mac', 'app')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # 如果是超级用户，显示所有条目
        return qs.filter(owner=request.user)  # 根据数据的所有者过滤条目

admin.site.register(channel)
admin.site.register(customer_information, UserInformationAdmin)
