from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# Create your views here.
from .forms import CreateUserForm, OrderForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *

#  -----------------HOME PAGE-----------------
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    # passing users into context 
    orders = Order.objects.all()
    products = Product.objects.all()
    context = {'orders': orders, 'products': products}
    return render(request, 'home.html', context)





# -----------------LOGIN PAGE-----------------
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username =request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')


    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



# -----------------REGISTER PAGE-----------------
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username =form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'register.html' , context)

@unauthenticated_user
def admin_register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username =form.cleaned_data.get('username')

            group = Group.objects.get(name='admin')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'admin_register.html' , context)




#  -----------------USER PAGE-----------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def userPage(request):
    orders = request.user.order_set.all()
    print(orders)

    context = {'orders': orders}
    return render(request, 'user.html', context)



#  -----------------CART PAGE-----------------

def cart(request):
    context = {}
    return render(request, 'cart.html', context)




#  -----------------STATUS PAGE-----------------
def statusPage(request):
    context = {}
    return render(request, 'status.html', context)




# -----------------SHOPPING PAGE-----------------
def shoppingPage(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    context = { 'orders': orders, 'products': products}
    return render(request, 'shopping.html', context)


# -----------------CART PAGE-----------------
def cartPage(request):
    context = {
        'products': Product.objects.all(),
        'order': Order.objects.all()
    }
    return render(request, 'cart.html', context)


# -----------------DELETE PAGE-----------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deletePage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        product = Product.objects.get(name=name)
        product.delete()
        return redirect('cart')
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'delete.html', context)





#  -----------------UPDATE PAGE-----------------
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def updatePage(request):
#     orders = Order.objects.all()
#     products = Product.objects.all()
#     form = OrderForm()
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('cart')
#     context = {'form': form, 'orders': orders, 'products': products}
#     return render(request, 'update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        product = create_product(name, image, description, price)
        return redirect('shopping')
    return render(request, 'create.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatePage(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        new_name = request.POST.get('new_name')
        new_description = request.POST.get('description')
        new_price = request.POST.get('price')
        # Assuming 'image' is a FileField or ImageField
        new_image = request.FILES.get('image')

        # Get the product to update
        product = Product.objects.get(name=product_name)

        # Update the product
        product.name = new_name
        product.description = new_description
        product.price = new_price
        if new_image is not None:  # Only update the image if a new one was provided
            product.image = new_image
        product.save()

        return redirect('shopping')

    else:
        products = Product.objects.all()
        return render(request, 'update.html', {'products': products})
