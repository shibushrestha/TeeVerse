from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Product, Order, UserCart
import json


# This is the homepage which displays all the product in the database
def home(request,):
	product_list = Product.objects.all().order_by('date_added')
	paginator = Paginator(product_list, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	# Get the success message from the session
	messages_iter = messages.get_messages(request)
	success_message = None
	for message in messages_iter:
		if message.tags == 'success':
			success_message = message
			break
	
	context =  {'page_obj':page_obj, 'success_message':success_message,}
	return render(request, 'Myapp/home.html', context)

# This is the detail view of the products
def detail(request, product_slug):
	product = get_object_or_404(Product, slug=product_slug)
	messages_iter = messages.get_messages(request)
	success_message = None
	for message in messages_iter:
		if message.tags == 'success':
			success_message = message
			break
	context = {'product':product, 'success_message': success_message}

	return render(request, 'Myapp/detail.html', context)


# This view is for the order logic
@login_required
def order(request, product_slug):
	product = get_object_or_404(Product, slug=product_slug)
	if request.method == "POST":
		quantity = request.POST.get('quantity')
		context ={
			'product':product,
			'quantity':quantity,
		}
		return render(request, 'Myapp/order.html', context)
	else:
		return redirect("Myapp:detail", product_slug)

	
# The order conformation view
@require_POST
def order_confirmation(request, product_slug, quantity):
	user = request.user
	product = get_object_or_404(Product, slug=product_slug)
	order = Order(user=user, product=product, quantity=quantity, payment_method="Cash on delivery")
	order.save()
	return redirect("Myapp:home")


# This is the cart functionality
def cart(request):
	user = request.user
	# Getting UserCart if its creates or create the cart
	user_cart, created = UserCart.objects.get_or_create(user=user)
	# Getting the product from the fetch api
	if request.method == 'POST':
		data = json.loads(request.body)
		product = data['productId']
		#adding the product to the user_cart
		user_cart.product.add(product)		
		user_cart.save()
		messages.success(request, 'Item added to cart.')
		
		return render(request, 'Myapp/home.html')
	# If the method is GET, display the cart page.
	else:
		cart_items = user.usercart.product.all()
		if cart_items.count() == 0:
			context={'no_cart_items':"No items have been added to the cart."}
		else:
			context = {'cart_items': cart_items}
		return render(request, 'Myapp/cart.html', context)
