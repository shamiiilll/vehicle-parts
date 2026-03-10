


from django.shortcuts import render,redirect, get_object_or_404
from .forms import*
from .models import*
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from .models import Product

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, "index.html", {"products": products})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')


        # try:
        #     user_obj = User.objects.get(username=username)
        #     username = user_obj.username
        # except:
        #     messages.error(request, "User not found")
        #     return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request,"Invalid username ")
            return redirect('login')
        
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid password")
            return redirect('login')

    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email= request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if not username or not email or not password:
            messages.error(request,"All fields are required")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')

        user = User.objects.create_user(
           username=username,
            email=email,
            password=password,
            
        )
        send_mail(
            'Verify your account',
            'Your account created successfully',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def sell_part(request):

    if request.method == "POST":

        brand = request.POST.get("brand")
        part = request.POST.get("part")
        category = request.POST.get("category")
        condition = request.POST.get("condition")
        price = request.POST.get("price")
        description = request.POST.get("description")

        Product.objects.create(
               seller=request.user,
               category=category,
               brand=brand,
               part=part,
               condition=condition,
               description=description,
               price=price
        )
        
    return render(request,'seller.html')


def logout_view(request):
    logout(request)
    return redirect('home')
def shop(request):
    items = Product.objects.all()  
    return render(request, 'shop.html', {'items': items})
@login_required
def my_products(request):
    items = Product.objects.filter(seller=request.user)
    return render(request, "my_products.html", {"items": items})

@login_required
def delete_product(request, item_id):
    item = get_object_or_404(Product, id=item_id, seller=request.user)  
    if request.method == "POST":
        item.delete()
        return redirect('my_products')
    return render(request, 'confirm_delete.html', {'item': item})
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.save()
        return redirect("my_products")

    return render(request, "edit_product.html", {"product": product})
def sell_product(request):
    if request.method == "POST":
        category = request.POST.get("category")
        brand = request.POST.get("brand")
        part = request.POST.get("part")
        condition = request.POST.get("condition")
        description = request.POST.get("description")
        price = request.POST.get("price")

        product = Product(
            seller=request.user,
            category=category,
            brand=brand,
            part=part,
            condition=condition,
            description=description,
            price=price,
            
        )
        product.save()

        return redirect("home")   

    return render(request, "seller.html")
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product})