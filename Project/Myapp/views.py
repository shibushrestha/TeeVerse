from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
import json

from .models import Product, Order, UserCart


# This is the homepage which displays all the product in the database
def home(request,):
	product_list = Product.objects.all().order_by('date_added')
	paginator = Paginator(product_list, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	
	context =  {'page_obj':page_obj,}
	return render(request, 'Myapp/home.html', context)

# This is the detail view of the products
def detail(request, product_slug):
	product = get_object_or_404(Product, slug=product_slug)
	
	print(type(product.description))
	for key in product.description:
		print(key + ":" + product.description[key])
	context = {'product':product,}
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

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, messages.Message):
            return str(obj)
        return super().default(obj)
    
# This is the cart functionality
@login_required
def cart(request):
	user = request.user
	# Getting UserCart if its creates or create the cart
	user_cart, created = UserCart.objects.get_or_create(user=user)
	# Getting the product from the fetch api
	if request.method == 'POST':
		data = json.loads(request.body)
		product = data['productId']
		product = Product.objects.get(id=product)
		#adding the product to the user_cart
		if product in user_cart.product.all():
			cartitem = user_cart.cartitem_set.get(product=product)
			cartitem.quantity = cartitem.quantity + 1
			cartitem.save()
			messages.success(request, 'Item quantity added to cart')
		else:
			user_cart.product.add(product)		
			user_cart.save()
			messages.success(request, 'Item added to cart')

		# Get the success message from the session
		message_storage = messages.get_messages(request)
		# Get messages and convert to JSON
		messages_list = [str(message) for message in message_storage]
		json_message = json.dumps(messages_list, cls=MessageEncoder)		
		#return render(request, 'Myapp/home.html')
		return JsonResponse({"message" : json_message})
	# If the method is GET, display the cart page.
	else:
		cart_items = user.usercart.product.all()
		if cart_items.count() == 0:
			context={'no_cart_items':"No items have been added to the cart."}
		else:
			context = {'cart_items': cart_items}
		return render(request, 'Myapp/cart.html', context)
