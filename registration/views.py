from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from management.models import channel, customer_information

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  # 设置 Staff Status
            user.save()

            # 创建与用户名同名的 Channel
            channel.objects.create(channel=user.username, user=user)

            # 创建并分配 Channel 模型的自定义权限
            channel_content_type = ContentType.objects.get_for_model(channel)
            view_permission, created = Permission.objects.get_or_create(codename='can_view_channel_entries', name='Can view channel entries', content_type=channel_content_type)
            change_permission, created = Permission.objects.get_or_create(codename='can_change_channel_entries', name='Can change channel entries', content_type=channel_content_type)
            delete_permission, created = Permission.objects.get_or_create(codename='can_delete_channel_entries', name='Can delete channel entries', content_type=channel_content_type)
            add_permission, created = Permission.objects.get_or_create(codename='can_add_channel_entries', name='Can add channel entries', content_type=channel_content_type)

            user.user_permissions.add(view_permission, change_permission, delete_permission, add_permission)

            # 创建并分配 CustomerInformation 模型的自定义权限
            customer_info_content_type = ContentType.objects.get_for_model(customer_information)
            view_permission_info, created = Permission.objects.get_or_create(codename='can_view_customer_information', name='Can view customer information', content_type=customer_info_content_type)
            change_permission_info, created = Permission.objects.get_or_create(codename='can_change_customer_information', name='Can change customer information', content_type=customer_info_content_type)
            delete_permission_info, created = Permission.objects.get_or_create(codename='can_delete_customer_information', name='Can delete customer information', content_type=customer_info_content_type)
            add_permission_info, created = Permission.objects.get_or_create(codename='can_add_customer_information', name='Can add customer information', content_type=customer_info_content_type)

            user.user_permissions.add(view_permission_info, change_permission_info, delete_permission_info, add_permission_info)

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
