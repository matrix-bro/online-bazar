from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_app/', views.test_app, name='test_app'),

    path('item/<slug:slug>/', views.item_details, name='item-details'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('new_item/', views.new_item, name='new-item'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('item/<slug:slug>/delete/', views.delete_item, name='delete-item'),
    path('item/<slug:slug>/edit/', views.edit_item, name='edit-item'),

    path('browse/', views.browse_items, name='browse'),

    path('new_conversation/<slug:item_slug>/', views.new_conversation, name='new-conversation'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<uuid:pk>/messages/', views.conversation_messages, name='conversation-messages'),

]