from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import*
import json
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
def category(request):
    categories = Category.objects.filter(is_sub = False )
    active_category = request.GET('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
        context = {'categories': categories,'products':products,'active_category':active_category}
        return render(request, 'app/category.html',context)
def search(request):
    if request.method == "POST":
        searched= request.POST["searched"]
        keys= Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        try:
            customer = request.user
        except:
            customer = User.objects.create(user=request.user)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  # đúng cách cho object
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']  # chỉ dùng dict ở đây

    products = Product.objects.all()
    return render( request,'app/search.html',{"searched":searched,"keys":keys,'products': products, 'cartItems': cartItems})
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # hoặc 'home'
    else:
        form = CreateUserForm()
        
    context = {'form': form}
    return render(request, 'app/register.html', context)
def loginPage( request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate (request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect ('home')
        else: messages.info(request,'Tên đăng nhập hoặc tài khoản chưa đúng')
    context = {}
    return render(request, 'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        try:
            customer = request.user
        except:
            customer = User.objects.create(user=request.user)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items  # đúng cách cho object
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']  # chỉ dùng dict ở đây

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'app/home.html', context)

from django.shortcuts import render
from .models import *

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        try:
            customer = request.user
        except:
            customer = User.objects.create(user=request.user)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)  # Sửa từ `json.load` → `json.loads`
    
    productId = data['productId']
    action = data['action']  # Sửa lỗi: ' action ' → 'action' (không có khoảng trắng)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)