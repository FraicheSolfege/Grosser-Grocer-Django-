"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
        # registration/login pages
    path("login/", loginPage, name="login"),
    path("logout/", logoutUser, name="logout"),
    path("register/", register, name="register"),
        # user pages
    path("user/", userPage, name="user"),
    path("shopping/", shoppingPage, name="shopping"),
        # order pages
    path("cart/", cartPage, name="cart"),
    path("add-to-cart/<int:product_id>/", addToCart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", removeFromCart, name="remove_from_cart"),
    path("clear-cart/", clearCart, name="clear_cart"),
    path("checkout/", checkoutPage, name="checkout"),
    path("order-status", statusPage, name="status"),
        # admin pages
    path("admin-register/", admin_register, name="admin_register"),
    path("create-products", createPage, name="create"),
    path("update-products/", updatePage, name="update"),
    path("delete-products/", deletePage, name="delete"),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
