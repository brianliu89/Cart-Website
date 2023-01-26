from django.contrib import admin
from django.urls import path
from django.db.models import base
from silverwareApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login),
    path('logout', views.logout),
    # path('register', views.register),
    path('register_buyer', views.RegisterBuyerView.as_view()),
    path('photo/', views.index),
    path('', views.main.as_view()),
    path('products', views.products_page.as_view()),
    path('topics', views.topic_page.as_view()),
    path('product/<str:product_id>', views.product_detail),
    path('product_detail/<int:product_id>', views.ProductDetailView),
    path('wishlist', views.wishlist),
    path('checkout', views.checkout),
    # path('cart', views.shopping_cart),
    path('cart', views.cart_view),
    path('test', views.showtemplate),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 購物車
# 管理系統
# 搜尋功能
# 邀請碼
# 優惠卷