from django import forms
from .models import ContactQuery, Subscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactQuery
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'subject': forms.TextInput(attrs={'placeholder': 'What is this about?'}),
            'message': forms.Textarea(attrs={'placeholder': 'Tell us more...', 'rows': 5}),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

    def clean_email(self):
        # without this, resubmitting an already-subscribed email throws
        # an ugly IntegrityError instead of a clean form error
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email