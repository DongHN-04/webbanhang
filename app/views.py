from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def order_success(request):
    if request.user.is_authenticated:
        customer = request.user
        user_not_login = 'hidden'
        user_login = 'show'
        order = Order.objects.filter(customer=customer, complete=True).order_by('-date_order').first()
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        user_not_login = 'show'
        user_login = 'hidden'
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories, 'items':items,'order':order, 'cartItems':cartItems, 'user_not_login': user_not_login, 'user_login': user_login}    
    return render(request, 'app/order_success.html', context)

def detail(request):    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories, 'products': products, 'items': items, 'order': order, 'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/detail.html', context)

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories': categories, 'active_category': active_category, 'products': products}
    return render(request, 'app/category.html', context)

def search(request):
    if request.method == 'POST':
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__icontains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order["get_cart_items"]
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    return render(request,'app/search.html', {'categories': categories,"searched":searched, "keys":keys, 'products':products, 'cartItems':cartItems})

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công! Bạn có thể đăng nhập.')
            return redirect('login')
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories, 'form': form}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Ngăn admin đăng nhập vào trang khách hàng
            if user.is_staff or user.is_superuser:
                messages.error(request, "Bạn không có quyền đăng nhập tại đây.")
                return redirect('login')

            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không đúng.")
            return redirect('login')
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context = {'categories': categories, 'products':products, 'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories, 'items': items, 'order': order, 'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/cart.html', context)

def checkout(request):
    categories = Category.objects.filter(is_sub=False)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
        if request.method == 'POST':
            # Lưu trạng thái đơn hàng
            order.complete = True
            order.date_ordered = timezone.now()
            order.save()

            # Lấy dữ liệu từ form
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            mobile = request.POST.get('SDT')

            # Lưu shipping info
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=address,
                city=city,
                state=state,
                mobile=mobile,
            )

            return redirect('order_success')
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order["get_cart_items"]
        user_not_login = "show"
        user_login = "hidden"
    context = {'categories': categories, 'items': items, 'order': order, 'cartItems':cartItems,'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity+=1
    elif action == 'remove':
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('added', safe=False)