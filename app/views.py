from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from app.forms import ConversationMessageForm, EditItemForm, NewItemForm, SignUpForm, LoginForm
from app.models import Category, Conversation, Item

def index(request):
    items = Item.objects.filter(is_sold=False).order_by('-created_at')[:6]
    categories = Category.objects.all()

    return render(request, 'app/index.html', {
        'categories': categories,
        'items': items
    })

def test_app(request):
    return render(request, 'app/test_app.html')

def item_details(request, slug):
    item = get_object_or_404(Item, slug=slug)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(slug=slug)[:3]
    
    return render(request, 'app/item_details.html', {
        'item': item,
        'related_items': related_items
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Account created successfully. You can now login!")
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'app/signup.html', {
        'form': form
    })

class CustomLoginView(LoginView):
    template_name = "app/login.html"
    authentication_form = LoginForm

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        messages.add_message(self.request, messages.INFO, "Login Successfull.")
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('login')
        
        messages.add_message(self.request, messages.INFO, "Logged out successfully.")
        return super().dispatch(request, *args, **kwargs)

@login_required
def new_item(request):
    if request.method == 'POST':
        # Not allowing users who belongs to Test App Group to create products
        if request.user.groups.filter(name='Test App Group').exists():
            messages.add_message(request, messages.INFO, "You don't have permission to create products.")
            return redirect('login')
        
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            # before saving, we also need to fill created_by field which is not coming from item_form so
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            messages.add_message(request, messages.INFO, "Product added successfully.")
            return redirect('item-details', slug=item.slug)
    else:
        form = NewItemForm()

    return render(request, 'app/item_form.html', {
        'form': form,
        'title': 'Add New Product',
    })

@login_required
def dashboard(request):
    items = Item.objects.filter(created_by=request.user).order_by('-created_at')

    return render(request, 'app/dashboard.html', {
        'items': items,
    })

@login_required
def delete_item(request, slug):
    if request.user.groups.filter(name='Test App Group').exists():
        messages.add_message(request, messages.INFO, "You don't have permission to delete products.")
        return redirect('login')
    
    item = get_object_or_404(Item, slug=slug, created_by=request.user)
    item.delete()
    messages.add_message(request, messages.INFO, "Product deleted successfully.")
    return redirect('dashboard')

@login_required
def edit_item(request, slug):
    item = get_object_or_404(Item, slug=slug, created_by=request.user)

    if request.method == 'POST':
        # Not allowing users who belongs to Test App Group to edit product details
        if request.user.groups.filter(name='Test App Group').exists():
            messages.add_message(request, messages.INFO, "You don't have permission to edit product details.")
            return redirect('login')
        
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Product details updated successfully.")
            return redirect('item-details', slug=item.slug)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'app/item_form.html', {
        'form': form,
        'title': 'Edit Product',
    })

def browse_items(request):
    query = request.GET.get('query', '')
    category_slug = request.GET.get('category', '') # to highlight the category
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if query:
        # Filtering in name OR description
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_slug:
        items = items.filter(category__slug=category_slug)

    return render(request, 'app/browse_items.html', {
        'items': items,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
    })

@login_required
def new_conversation(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)

    # person who created this item, can't create a new conversation
    # it should be other users
    if item.created_by == request.user:
        return redirect('dashboard')
    
    # if this user already has a conversation or has already messaged this owner then redirect to that old conversation
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation-messages', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # first create a conversation and then conversation message

            conversation = Conversation.objects.create(item=item)

            # add the owner and the user who messaged to the members list
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation-messages', pk=conversation.id)
    else:
        form = ConversationMessageForm()

    return render(request, 'app/new_conversation.html', {
        'form': form,
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'app/inbox.html', {
        'conversations': conversations
    })

@login_required
def conversation_messages(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save() # update modified_date of conversation

            return redirect('conversation-messages', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'app/conversation_messages.html', {
        'conversation': conversation,
        'form': form,
    })