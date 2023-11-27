from django.shortcuts import get_object_or_404, render

from app.models import Category, Item

def index(request):
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()

    return render(request, 'app/index.html', {
        'categories': categories,
        'items': items
    })

def item_details(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    
    return render(request, 'app/item_details.html', {
        'item': item,
        'related_items': related_items
    })

def contact(request):
    return render(request, 'app/contact.html')