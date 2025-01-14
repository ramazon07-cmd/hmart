from django.urls import path
from .views import *

urlpatterns = [
	path('', home, name='home'),
	path('about/', about, name='about'),
	path('category/<category_name>/', categories, name='categories'),
	path('product/<product_id>/', product_detail, name='product_detail'),
	path('products/', products, name='products'),
	path('contact/', CreateContactView.as_view(), name='contact'),
	path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', remove_from_wishlist, name='remove_from_wishlist'),
	path('search/', search, name='search'),
	path('cart/', cart_view, name='cart'),
	path('checkout/', checkout, name='checkout'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
]
