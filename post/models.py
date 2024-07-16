from django.db import models
from pathlib import Path
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.utils.timezone import now
# Create your models here.

def get_image_path(instance,filename):
    return Path('images')/ str(instance.id)/filename

class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(blank=True,null=True,upload_to='fotos/')
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title  

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createsd_at = models.DateTimeField(default=now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"