from django.shortcuts import render

from app.models import Category, Item

def index(request):
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()

    return render(request, 'app/index.html', {
        'categories': categories,
        'items': items
    })

def contact(request):
    return render(request, 'app/contact.html')