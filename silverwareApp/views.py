from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, LoginForm, UploadModelForm
from django.views import View
from django.urls import reverse
from .models import product, MyUser, Cart
from django.contrib import auth
from django.contrib.auth.models import User, Group
from silverwareApp.vars import *
from datetime import datetime, timedelta
from silverwareApp import factory
import re
from django.views.generic import ListView, TemplateView
import base64
import pickle
from django.http import JsonResponse
# from silverwareApp.templatetags.filter import *

email_re = r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$'
phone_re = r'\+?(\#|\*|\d)*'


def get_context():
    return {'types': types, 'topics': topics, }

def index(request):
    photos = product.objects.all()  # 查詢所有資料
    form = UploadModelForm()
    if request.method == "POST":
        form = UploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('/products')
    context = {
        'photos': photos,
        'form': form
    }


def showtemplate(request):
    # product_list = product.objects.all()
    # context = {'product_list': product_list}
    form = UploadModelForm()
    context = {
        'form': form
    }

    return render(request, 'test.html', context)


class main(ListView):
    # context = get_context()
    # context['banner_list'] = home_banner_list
    # context['promote_products'] = factory.get_FE_products(
    #     {p_id: products[p_id] for p_id in home_promote_product_id_list})
    # context['promote_section_title'] = home_promote_section_title
    # context['promote_section_subtitle'] = home_promote_section_subtitle
    # product_list = product.objects.all()
    # context['product_list'] = product_list
    #
    # return render(request, 'home.html', context)
    model = product
    paginate_by = 8
    template_name = "home.html"

class products_page(ListView):
    # context = get_context()
    # product_list = product.objects.all()
    #
    # paginator = Paginator(product_list, 4)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # context['page_obj'] = page_obj
    #
    # context['product_title'] = '所有商品'
    # context['tags'] = tags
    # context['products'] = factory.get_FE_products(products)
    # context = {'product_list': product_list}
    #
    # return render(request, 'shop-page-grid.html', context)
    model = product
    paginate_by = 12
    template_name = "shop-page-grid.html"

class topic_page(ListView):
    model = product
    paginate_by = 12
    template_name = "topic-page.html"

def product_detail(request, product_id):
    context = get_context()

    # print(product_id)

    # context['product_title'] = '所有商品'
    # context['tags'] = tags
    # get product from model Product
    context['product'] = factory.get_product(product_id)
    # print(context['product'])

    return render(request, 'product-detail.html', context)

def ProductDetailView(request, product_id):
    context = get_context()
    product_list = product.objects.filter(id = product_id)
    context['product_list'] = product_list

    product_list = product.objects.get(id=product_id)
    product_list.watched += 1
    product_list.save()

    products = product.objects.order_by('?').filter(group='銀飾類')[0:4]
    context['products'] = products
    return render(request, 'product-detail.html', context)

def checkout(request):
    context = get_context()

    return render(request, 'checkout.html', context)

def shopping_cart(request):
    context = get_context()

    return render(request, 'shopping-cart.html', context)

def wishlist(request):
    context = get_context()

    return render(request, 'wishlist.html', context)


# Reference of register and login
# https://docs.djangoproject.com/en/4.1/topics/auth/default/
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/

# def register(request):
#     if request.method == 'POST':
#         print(request.POST)
#         username = ''
#         email = request.POST['email']
#         password = request.POST['password'] # encrypt?
#         user = User.objects.create_user(username, email, password)

# def register(request):
#     form = RegisterForm()
#
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')  # 重新導向到登入畫面
#
#     context = {'form': form}
#     return render(request, '/', context)

class RegisterBuyerView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        first_name = request.POST['first_name'].strip()
        phone = request.POST['phone'].strip()  # 需檢查電話格式, 是否有效(以驗證碼處理), 是否已被註冊, 完成
        email = request.POST['email'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()

        messages = []
        if phone and not re.match(phone_re, phone):
            messages.append('電話格式不符')
        if User.objects.filter(username=phone):
            messages.append('此電話號碼已被註冊')
        if not re.match(email_re, email):
            messages.append('電子郵件格式不符')
        if password1 != password2:
            messages.append('密碼不一致')
        if messages:
            return render(request, self.template_name, {'messages': messages,
                                                        'email': email,
                                                        'first_name': first_name,
                                                        'phone': phone,
                                                        'email': email})

        user = User.objects.create_user(username=phone, password=password1)
        MyUser.objects.create(user=user, password=password1, name=first_name, phone=phone, address=email)
        return render(request, self.template_name)

# def CartAddView(request):
#     try:
#         data = request.GET.dict()
#         data['productId'] = product.objects.get(id=data['productId'])
#         data['uid'] = MyUser.objects.get(id=request.session.get['uid'])
#         ob = Cart.objects.filter(uid=data['uid']).filter(productId=data['productId'])
#         if ob.count():
#             cart = Cart.objects.get(id=ob[0].id)
#             cart.num += int(data['num'])
#             cart.save()
#         else:
#             ob = Cart(**data)
#             ob.save()
#         return render(request, 'home.html')
#     except:
#         pass
#     return render(request, 'home.html')

def cart_view(request):
    cart_list = Cart.objects.all()
    context = get_context()
    context['cart_list'] = cart_list
    return render(request, 'shopping-cart.html', context)

def login(request):
    form = LoginForm()

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect('/products')  # 重新導向到登入畫面

    context = {'form': form}
    return render(request, 'home.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')