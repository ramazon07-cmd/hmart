from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)

admin.site.register(Photos)

admin.site.register(Category)

admin.site.register(Contact)

admin.site.register(Wishlist)

admin.site.register(Cart)

admin.site.register(Order)
