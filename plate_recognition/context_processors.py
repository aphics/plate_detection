from django.conf import settings


def app_title(request):
    return {"APP_TITLE": settings.APP_TITLE}
