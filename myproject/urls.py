from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # 修正路径格式，确保尾部有 "/"
    path('api/apk/', include('appp.urls')),    # 修正路径并正确传递 include()
    path('registration/', include('registration.urls')),
    path('management/', include('management.urls')),
    path('connection/',include('connection_stack.urls')),
    path('customer/',include('management.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
