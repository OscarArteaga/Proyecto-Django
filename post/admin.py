from django.contrib import admin
from post.models import Post, Order, OrderItem

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Order)
admin.site.register(OrderItem)