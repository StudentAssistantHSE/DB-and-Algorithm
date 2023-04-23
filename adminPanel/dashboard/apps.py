from django.apps import AppConfig


class CustomAuthConfig(AppConfig):
    name = 'django.contrib.auth'
    verbose_name = 'Роли'

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminPanel.dashboard'
    verbose_name = 'Данные'
