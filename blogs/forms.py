from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core import validators

class RegisterForm(UserCreationForm):
    email = forms.EmailField(help_text='Please enter a valid email address')
    password1 = forms.CharField(
        label='Password',
        help_text='Password must contain at least eight characters,at least one number and both lower and uppercase letters and special characters',
        widget=forms.PasswordInput,
        min_length=8,
        validators=[
            validators.RegexValidator(
                regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}$",
                message='Password must contain at least eight characters,at least one number and both lower and uppercase letters and special characters'
            ),
        ]

    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password2'].help_text = 'Enter the same password as above, for verification.'
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 150:
            raise forms.ValidationError('Username must be 150 characters or fewer')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'This username is already taken. Please choose a different username.')
        return username

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email already exists!')

            # raise forms.ValidationError('Email already exists!')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2