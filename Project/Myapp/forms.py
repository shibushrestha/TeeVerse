from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from Myapp.models import User

class UserRegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'unique_email': _("This email address is already in use."),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':'Username', 'autofocus': False, 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder':'Enter your email address', 'autofocus':False, 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Enter a password', 'class': 'form-control password-input',})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm password', 'class': 'form-control password-input',})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['unique_email'],
                code='unique_email',
            )
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')
    error_messages={
        'invalid_login': 'Please enter a correct username or email and password'
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the widget for the username field to a TextInput
        self.fields['username'].widget.attrs.update({'placeholder':'Username or email address', 'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder':'Enter your password', 'class': 'form-control password-input'})