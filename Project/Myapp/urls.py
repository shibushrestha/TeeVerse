from django.urls import re_path, path
from Myapp import views, useraccountviews
from Myapp.useraccountviews import UserPasswordChange, EditUserProfile, CustomLoginView, CustomLogoutView


app_name = 'Myapp'

urlpatterns=[
	re_path(r'^$', views.home, name='home'),
	re_path(r'^(?:product-(?P<product_slug>[A-za-z0-9-]+)/)?$', views.detail, name='detail'),
	re_path(r'^order/(?P<product_slug>[A-Za-z0-9-]+)/$', views.order, name='order'),
	re_path(r'^orderconfirmation/(?P<product_slug>[A-Za-z0-9-]+)/(?P<quantity>[\d]+)/$', views.order_confirmation, name='order-confirm'),
	re_path(r'^cart/$', views.cart, name='cart'),
	
	re_path(r'^register/$', useraccountviews.register, name='user-register'),

	re_path(r'^login/$', CustomLoginView.as_view(), name='login'),
	re_path(r'^logout/$', CustomLogoutView.as_view(), name='logout'),
	re_path(r'^(?P<user_username>[a-zA-Z0-9!@$_.]+)/$', useraccountviews.user_profile, name='userprofile'),
    re_path(r'^(?P<user_username>[a-zA-Z0-9!@$_.]+)/changepassword/$', UserPasswordChange.as_view(), name='changepassword'),
	re_path(r'^(?P<user_username>[a-zA-Z0-9!@$_.]+)/editprofile/$', EditUserProfile.as_view(), name='edit-profile'),

]