from django.shortcuts import render, redirect
from app.models import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def account(request):
	wishlist_items = Wishlist.objects.filter(user=request.user)
	cart_items = Cart.objects.filter(user=request.user)
	orders = Order.objects.filter(first_name=request.user.first_name)

	context = {
		'wishlist_items': wishlist_items,
		'cart_items': cart_items,
		'orders': orders,
	}
	return render(request, 'account.html', context)

def login_signup_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            # Handle login
            login_form = LoginForm(request.POST)
            signup_form = SignupForm()
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials')
        elif 'signup' in request.POST:
            # Handle signup
            login_form = LoginForm()
            signup_form = SignupForm(request.POST, request.FILES)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')
    else:
        login_form = LoginForm()
        signup_form = SignupForm()

    return render(request, 'account/login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })

@login_required
def instant_logout(request):
    logout(request)
    return redirect('home')
