from django.urls import path
from app.views import index, contact
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)