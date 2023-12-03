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
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('new_item/', views.new_item, name='new-item'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete-item'),
    path('item/<int:pk>/edit/', views.edit_item, name='edit-item'),

    path('browse/', views.browse_items, name='browse'),

    path('new_conversation/<int:item_pk>/', views.new_conversation, name='new-conversation'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:pk>/messages/', views.conversation_messages, name='conversation-messages'),

]