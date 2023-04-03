from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
import shortuuid
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email and username as unique identifiers.
    """
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_property_admin = models.BooleanField(_('property admin'), default=False, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, editable=False)
    profile_image = models.ImageField(_('profile image'), upload_to='Myapp/User/profile_image/', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        #Returns the short name for the user.
        return self.first_name

    def __str__(self):
        """
        String representation of the user model.
        """
        return self.username

# The Product model
class Product(models.Model):
	Tshirt_Type = [
		('K', 'Kids'),
		('A', 'Adults'),
    ]
	name = models.CharField(max_length=100)
	description = models.JSONField(blank=True)
	price = models.IntegerField(default = 0)
	product_image = models.ImageField(upload_to= 'Myapp/products/images')
	tshirt_type = models.CharField(max_length=1, choices=Tshirt_Type,)
	date_added = models.DateTimeField(auto_now=True)
	slug = models.SlugField(blank=True)
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse("Myapp:detail", kwargs={"product_slug": self.slug})
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)


# User reviewing the product.
class Review(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	review = models.CharField(max_length=1000)
	

# The order users are gonna make
class Order(models.Model):
	order_id = models.CharField(max_length=22, default='')	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveSmallIntegerField()
	ordered_datetime = models.DateTimeField(auto_now_add=True)
	# Payment Choices(for now only Cash on delivery is being implemented)
	class PaymentChoice(models.TextChoices):
		CASH_ON_DELIVERY = 'C',_('Cash on delivery')
		OTHERS = 'O',_('others')
	payment_method = models.CharField(max_length=1, choices=PaymentChoice.choices, default="C")
	# Status of the order
	class OrderStatus(models.TextChoices):
		DELIVERED = 'D',_('Delivered')
		ON_THE_WAY = 'OTW',_('On the way')
		CANCELLED = 'C',_('Cancelled')
	order_status = models.CharField(max_length=3, choices=OrderStatus.choices, blank=True)
	
	# Individual total of a product and its quantity
	@property
	def get_order_total(self):
		total = self.product.price * self.quantity
		return total
	
	def __str__(self):
		return str(self.order_id) + '  ' + self.user.username+ '  ' + self.product.name+ '  ' + str(self.quantity)
	
''' 
We are setting the order_id for the Order model after listening to the pre_save signal
because if we provide the shortuuid as default in the order_id field of the model, everytime we run makemigrations
it creates a new migration for the Order model as the value for the shortuuid will always be different
'''
@receiver(pre_save, sender=Order)
def set_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = shortuuid.uuid()
	

# The cart for an user	
class UserCart(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	product = models.ManyToManyField(Product, verbose_name="cart items",
		through='CartItem',
		through_fields=('cart', 'product')
		)
	@property
	def get_cart_total(self):
		total = sum([items.price for items in self.product.all()])
		return total
	
	def __str__(self):
		return self.user.username + "'s cart"

class CartItem(models.Model):
	cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveSmallIntegerField(default=1)

# This is a proxy model that deals with the orders the user made.
class UserOrder(User):
	class Meta():
		proxy = True

	# To get the total of all the orders the user made
	@property
	def get_total_of_all_orders(self):
		all_orders = self.order_set.all()
		individual_total = [order.get_order_total for order in all_orders]
		total_of_all_orders = sum(num for num in individual_total)
		return total_of_all_orders
