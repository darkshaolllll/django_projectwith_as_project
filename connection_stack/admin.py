from django.contrib import admin
from .models import requestion_of_ali

@admin.register(requestion_of_ali)
class admin_of_alirequestion(admin.ModelAdmin):
    list_display = ('id', 'mac', 'app')
