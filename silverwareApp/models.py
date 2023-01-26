from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User

GROUP = (('銀飾類', '銀飾類'), ('生活類', '生活類'), ('其他', '其他'))

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=20, verbose_name='密碼', null=True)
    name = models.CharField(max_length=20, verbose_name='姓名', null=True)
    phone = models.CharField(max_length=10, verbose_name='電話', null=True)
    address = models.CharField(max_length=50, verbose_name='電子郵件', null=True)

# 購買者購物車
class Cart(models.Model):
    uid = models.ForeignKey(to="MyUser", to_field="id", on_delete=models.CASCADE, verbose_name='用戶ＩＤ')
    productId = models.ForeignKey(to="product", to_field="id", on_delete=models.CASCADE, verbose_name='商品ＩＤ')
    num = models.IntegerField(default=0, verbose_name='數量')
    sum = models.IntegerField(default=0, verbose_name='總額')

class product(models.Model):
    product_title = models.CharField(max_length=35, verbose_name='商品名稱')
    price = models.IntegerField(default=0, verbose_name='商品價格')
    watched = models.IntegerField(default=0, verbose_name='觀看次數')
    inventory = models.CharField(max_length=20, verbose_name='庫存')
    is_soldout = models.CharField(max_length=20, verbose_name='已賣出')
    discount = models.IntegerField(default=10, verbose_name='折扣(1~9)')
    description = models.TextField(blank=True, verbose_name='商品描述')
    tag = models.CharField(max_length=20, blank=True, verbose_name='標籤')
    image = models.ImageField(upload_to='', blank=True, null=True, verbose_name='商品圖片')
    # create_time = models.DateTimeField(default=timezone.now, blank=True, verbose_name='上架時間')
    new = models.BooleanField(default=True, verbose_name='新品上市')
    group = models.CharField(max_length=10, choices=GROUP, null=True, verbose_name='分類')
    upload_date = models.DateField(default=timezone.now, verbose_name='更新日期')

    def get_absolute_url(self):
        return reverse("vendor_id", kwargs={"id": self.id})

    # 覆寫 __str__
    def __str__(self):
        return self.product_title

@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'price', 'watched', 'inventory', 'is_soldout')
    # list_display = [field.name for field in product._meta.fields]
    # list_filter = ('vendor_name',)
    # field = ['phone_number'] # 顯示欄位
    # search_fields = ('food_name','price_name') # 搜尋欄位
    # ordering = ('price_name',) # 價格 由小到大 排序, 新增 -，資料改為 由大到小 排序