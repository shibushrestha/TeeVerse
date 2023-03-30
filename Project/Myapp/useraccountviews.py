from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Myapp.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from Myapp.forms import UserRegistrationForm, CustomAuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Myapp:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'Myapp/register.html', {'form': form})



class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'Myapp/login.html'
    success_url = reverse_lazy('Myapp:home')
    def form_valid(self, form):
        # Call the parent form_valid method to log the user in
        response = super().form_valid(form)

        # Construct the URL of the view to redirect to after login
        next_url = self.request.GET.get('next')

        # If the user should be redirected to the view that only accepts POST requests,
        # construct a POST request and return it
        if next_url:
            return HttpResponse(status=308, headers={'Location': next_url,})
        # Otherwise, return the default redirect response
        return response



        
class CustomLogoutView(LogoutView):
    success_url = reverse_lazy('Myapp:home')


# This view is for user profile
@login_required
def user_profile(request, user_username):
    user = get_object_or_404(User, username = user_username)
    if user == request.user:
        context = {'user':user}
        return render(request, 'Myapp/useraccount.html', context)
    else:
        return redirect("Myapp:login")

# This view is for the password change view.
class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'Myapp/change-password.html'
    success_url = '/Myapp/login/'


class EditUserProfile(UpdateView):
    template_name = 'Myapp/edit-profile.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = User.objects.get(pk = self.id)
        return queryset
        