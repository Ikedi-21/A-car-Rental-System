from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Extends Django's UserCreationForm to also capture email, first/last
    name, and phone at registration — phone gets saved to Profile in the
    view's save(), since it doesn't live on the User model itself.
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def clean_email(self):
        # UserCreationForm doesn't enforce unique email by default (only
        # username), and we're treating email as the practical identifier
        # per the CRS, so this needs its own check
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email