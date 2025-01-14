from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def home(request):
	products = Product.objects.all()
	wishlist_items = Wishlist.objects.filter(user=request.user)
	cart_items = Cart.objects.filter(user=request.user)

	context = {
		'products': products,
		'wishlist_items': wishlist_items,
		'cart_items': cart_items
	}
	return render(request, 'home.html', context)

def products(request):
	products = Product.objects.all()
	wishlist_items = Wishlist.objects.filter(user=request.user)
	cart_items = Cart.objects.filter(user=request.user)

	context = {
		'products': products,
		'wishlist_items': wishlist_items,
		'cart_items': cart_items
	}
	return render(request, 'products.html', context)

def categories(request, category_name):
	products = Product.objects.filter(category__name=category_name)
	wishlist_items = Wishlist.objects.filter(user=request.user)
	cart_items = Cart.objects.filter(user=request.user)

	context = {
		'products': products,
		'wishlist_items': wishlist_items,
		'cart_items': cart_items
	}
	return render(request, 'products.html', context)

def about(request):
	contacts = Contact.objects.all()
	wishlist_items = Wishlist.objects.filter(user=request.user)
	cart_items = Cart.objects.filter(user=request.user)

	context = {
		'contacts': contacts,
		'wishlist_items': wishlist_items,
		'cart_items': cart_items
	}
	return render(request, 'about.html', context)

def product_detail(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	wishlist_items = Wishlist.objects.filter(user=request.user)
	related_products = Product.objects.all()[:4]
	cart_items = Cart.objects.filter(user=request.user)
	photos = product.photos.all()

	context = {
		'product': product,
		'wishlist_items': wishlist_items,
		'cart_items': cart_items,
		'photos': photos,
		'related_products': related_products,
	}
	return render(request, 'product_detail.html', context)

class CreateContactView(SuccessMessageMixin, CreateView):
    model = Contact
    form_class = CreateContactForm
    template_name = 'contact.html'
    success_url = '/'
    success_message = 'Created'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['wishlist_items'] = Wishlist.objects.filter(user=self.request.user)
            context['cart_items'] = Cart.objects.filter(user=self.request.user)
        else:
            context['wishlist_items'] = None
            context['cart_items'] = None
        return context


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=request.user)

    context = {
        'wishlist_items': wishlist_items,
        'cart_items': cart_items,
    }

    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        return redirect('home')
    else:
        return redirect('home')

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect('home')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if created:
        return redirect('home')
    else:
        return redirect('home')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('home')

# def checkout(request):
# 	wishlist_items = Wishlist.objects.filter(user=request.user)
# 	cart_items = Cart.objects.filter(user=request.user)
#
# 	context = {
# 		'wishlist_items': wishlist_items,
# 		'cart_items': cart_items
# 	}
# 	return render(request, 'checkout.html', context)

@login_required
def checkout(request):
	user = request.user
	wishlist_items = Wishlist.objects.filter(user=request.user)
	cart_items = Cart.objects.filter(user=request.user)
	total_price = sum(item.product.price for item in cart_items)

	if request.method == "POST":
	    form = CheckoutForm(request.POST)
	    if form.is_valid():
	        order = Order.objects.create(
	            first_name=form.cleaned_data['first_name'],
	            last_name=form.cleaned_data['last_name'],
	            country=form.cleaned_data['country'],
	            street_address=form.cleaned_data['street_address'],
	            city=form.cleaned_data['city'],
	            state=form.cleaned_data['state'],
	            postcode=form.cleaned_data['postcode'],
	            phone=form.cleaned_data['phone'],
	            email=form.cleaned_data['email'],
	            total_price=total_price
	        )
	        cart_items.delete()
	        return redirect('home')

	else:
	    form = CheckoutForm()

	context = {
		'user': user,
		'form': form,
		'cart_items': cart_items,
    	'total_price': total_price,
		'shipping_cost': 0,
    }

	return render(request, 'checkout.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(about__icontains=query)
        )
    return render(request, 'products.html', {'query': query, 'products': products})
