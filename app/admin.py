from django.contrib import admin

from app.models import Category, Conversation, ConversationMessage, Item

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Conversation)
admin.site.register(ConversationMessage)