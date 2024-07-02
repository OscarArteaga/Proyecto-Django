"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path,include
from post.api.router import router_posts
from post.views import index , agregar, editar, eliminar , register , user_login , eliminar_del_carrito , agregar_al_carrito , ver_carrito , detalles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router_posts.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', index, name='index'),
    path('register/', register, name='register' ),
    path('login/', user_login, name='login'),
    path('agregar/', agregar, name='agregar'),
    path('editar/<int:pk>/', editar, name='editar'),
    path('eliminar/<int:pk>/', eliminar, name='eliminar'),
    path('agregar_al_carrito/<int:post_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('producto/<int:pk>/',detalles,name='detallesProducto'),
    path('eliminar_del_carrito/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
