from django.contrib import admin
from .models import apk_information, requestion_information

@admin.register(apk_information)
class ApkInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','packagename', 'version')

@admin.register(requestion_information)
class RequestionInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time', 'ip')
