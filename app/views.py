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
    return render(request, 'app/item_details.html', {
        'item': item
    })

def contact(request):
    return render(request, 'app/contact.html')