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


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    # passing users into context 
    orders = Order.objects.all()
    products = Product.objects.all()
    context = {'orders': orders, 'products': products}
    return render(request, 'home.html', context)

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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def userPage(request):
    orders = request.user.order_set.all()
    print(orders)

    context = {'orders': orders}
    return render(request, 'user.html', context)

def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def statusPage(request):
    context = {}
    return render(request, 'status.html', context)

def shoppingPage(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    context = { 'orders': orders, 'products': products}
    return render(request, 'shopping.html', context)