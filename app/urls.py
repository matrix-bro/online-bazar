from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('item/<int:pk>/', views.item_details, name='item-details'),

    path('signup/', views.signup, name='signup'),

]