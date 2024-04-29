from django.apps import AppConfig

class MycoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MyCourses'

    def ready(self):
        try:
            from mailing_script import send_mailing
            import mailings.tasks  # Импорт задач для их регистрации в планировщике
        except ImportError:
            pass
