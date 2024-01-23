from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import uuid
from django.utils.text import Truncator

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    is_sold = models.BooleanField(default=False)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    image_card = ImageSpecField(source='image', processors=[ResizeToFill(450, 250)], format='PNG', options={'quality': 100})
    slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item-details', kwargs={"slug": self.slug})
    
    def generate_unique_slug(self):
        slug = slugify(self.name)
        
        unique_slug = slug 
        # if the slug is unique, we will return that slug
        # if not unique, we will generate unique slug

        num = 1
        while Item.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        
        return unique_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)

    
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at', )

    def __str__(self):
        return f"Conversation about Item: {self.item} between {' & '.join(self.members.all().values_list('username', flat=True))}"

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.created_by} --- to --- {self.conversation.members.exclude(username=self.created_by).first()} ------ {Truncator(self.content).words(5)}"