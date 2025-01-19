from django.apps import AppConfig


class App1QConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appp'
    def ready(self):
        import appp.signals  # 确保信号在应用启动时被注册

