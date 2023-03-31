from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Product, Order, Review, UserCart, CartItem

class UserAdmin(UserAdmin):
    # Exclude last_login from the fields displayed in the form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # Exclude last_login from the list of fields to display in the changelist
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',)

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(UserCart)
admin.site.register(CartItem)




