from django.shortcuts import get_object_or_404, redirect, render
from app.forms import EditItemForm, NewItemForm, SignUpForm
from django.contrib.auth.decorators import login_required
from app.models import Category, Item

def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[:6]
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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'app/signup.html', {
        'form': form
    })

@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            # before saving, we also need to fill created_by field which is not coming from item_form so
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item-details', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'app/item_form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def dashboard(request):
    items = Item.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, 'app/dashboard.html', {
        'items': items,
    })

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard')

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item-details', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'app/item_form.html', {
        'form': form,
        'title': 'Edit Item',
    })

def browse_items(request):

    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    return render(request, 'app/browse_items.html', {
        'items': items,
        'categories': categories,
    })