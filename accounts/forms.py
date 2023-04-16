from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EmailValidator, ValidationError
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from django.contrib.auth import authenticate


class CustomAuthenticationForm(AuthenticationForm):
    email_or_phone = forms.CharField(
        label='Email or Phone',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')  # Remove the default 'username' field

    def clean(self):
        email_or_phone = self.cleaned_data.get('email_or_phone')
        password = self.cleaned_data.get('password')

        if email_or_phone and password:
            self.user_cache = authenticate(self.request, email_or_phone=email_or_phone, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid login credentials.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data



class CustomUserCreationForm(UserCreationForm):
    email_or_phone = forms.CharField(label="Email or Phone", max_length=254)

    class Meta:
        model = CustomUser
        fields = ("email_or_phone", "password1", "password2")

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data["email_or_phone"]
        if "@" in email_or_phone:
            validate_email = EmailValidator()
            try:
                validate_email(email_or_phone)
                if CustomUser.objects.filter(email=email_or_phone).exists():
                    raise forms.ValidationError("Email already exists.")
                return {"email": email_or_phone}
            except ValidationError:
                raise forms.ValidationError("Invalid email address.")
        else:
            if CustomUser.objects.filter(phone=email_or_phone).exists():
                raise forms.ValidationError("Phone number already exists.")
            return {"phone": email_or_phone}

    def save(self, commit=True):
        user = super().save(commit=False)
        email_or_phone = self.cleaned_data["email_or_phone"]
        if "email" in email_or_phone:
            user.email = email_or_phone["email"]
        else:
            user.phone = email_or_phone["phone"]
        if commit:
            user.save()
        return user
