from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from app.forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('item/<int:pk>/', views.item_details, name='item-details'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),

]