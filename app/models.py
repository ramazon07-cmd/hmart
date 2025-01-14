from django.db import models
from django.conf import settings

class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Photos(models.Model):
	photo = models.ImageField(upload_to='photos/')

	def __str__(self):
		return f"{self.id}"

class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	slug = models.CharField(max_length=255)
	price = models.DecimalField(decimal_places=2, max_digits=15)
	general = models.ImageField(upload_to='photos/')
	photos = models.ManyToManyField(Photos)
	about = models.TextField()

	def __str__(self):
		return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.product.name}"


class Contact(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	phone = models.CharField(max_length=12)
	message = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.first_name} {self.last_name}"
