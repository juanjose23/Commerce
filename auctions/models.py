from django.contrib.auth.models import AbstractUser
from django.db import models
import os
import uuid
from django.utils.text import slugify

def upload_to(instance, filename):
    # Generar un nombre de archivo único usando uuid4
    ext = filename.split('.')[-1]  # Obtener la extensión del archivo
    new_filename = f"{uuid.uuid4()}.{ext}"  # Crear un nuevo nombre de archivo único
    return os.path.join('Listing/images/', new_filename)

class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True) 
    description = models.TextField(blank=True, null=True) 
    def save(self, *args, **kwargs):
            if not self.slug:
                base_slug = slugify(self.name)
                slug = base_slug
                num = 1
                while Category.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{num}"
                    num += 1
                self.slug = slug
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Listing(models.Model):
    ACTIVE = 1
    INACTIVE = 2

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True, blank=True)  # Usar SlugField y establecer unique=True
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name="listings")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Listing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def current_price(self):
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid.amount if highest_bid else self.starting_bid

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.listing}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.listing}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted")

    def __str__(self):
        return f"{self.user} is watching {self.listing}"
