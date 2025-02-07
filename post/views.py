from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .models import *
from .forms import FormularioJuego
from .forms import CustomUserCreationForm , CustomAuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login, authenticate
from django.db.models import Sum 
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .decorators import admin_required

# Create your views here.
def index(request):
    posts = Post.objects.all();
    return render(request,'index.html',{'posts':posts})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  
            user.save()
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@admin_required
def agregar(request):
    if request.method == "POST":
        form = FormularioJuego(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FormularioJuego()
    return render(request,'agregar.html',{'form': form})

@admin_required
def editar(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = FormularioJuego(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FormularioJuego(instance=post)
    return render(request,'editar.html',{'form': form})

def detalles(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'detalleProducto.html', {'post': post})

@admin_required
def eliminar(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('index')
    return render(request,'eliminar.html',{'post': post})

@login_required
def agregar_al_carrito(request, post_id):
    product = get_object_or_404(Post, id=post_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        items = cart.items.all()
        total = items.aggregate(total=Sum('product__price'))['total']
    else:
        items = []
        total = 0

    return render(request, 'carrito.html', {'items': items, 'total': total})

@login_required
def eliminar_del_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('ver_carrito')

@login_required
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart or cart.items.count() == 0:
        return redirect('ver_carrito')  

    total_amount = cart.items.aggregate(total=Sum('product__price'))['total']


    for cart_item in cart.items.all():
        product = cart_item.product
        if product.stock < cart_item.quantity:
            return redirect('ver_carrito')

    order = Order.objects.create(user=user, total_amount=total_amount)

    for cart_item in cart.items.all():
        product = cart_item.product
        if product.stock >= cart_item.quantity:
            product.stock -= cart_item.quantity
            product.save()
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        else:
            return redirect('ver_carrito')
        
    cart.items.all().delete()

    request.session['order_id'] = order.id
  
    return redirect('order_success')  

def order_success(request):
    return render(request, 'order_success.html')

def boleta(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    return render(request, 'boleta.html', {'order': order, 'order_items': order_items})