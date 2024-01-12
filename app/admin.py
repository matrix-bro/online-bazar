from django.contrib import admin

from app.models import Category, Conversation, ConversationMessage, Item

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Item, ItemAdmin)

admin.site.register(Conversation)
admin.site.register(ConversationMessage)