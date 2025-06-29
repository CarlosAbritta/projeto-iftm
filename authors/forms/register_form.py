from utils.django_forms import add_attr,add_placeholder,strong_password
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class RegisterForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'],'Your E-mail')
        add_placeholder(self.fields['first_name'],'Ex.:Tralalero')
        add_placeholder(self.fields['last_name'],'Ex.:Tralala')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            ]
        labels = {
        'username':'Username',
        'first_name':'First Name',
        'last_name':'Last Name',
        'email':'E-mail',
    }
        help_texts = {
        'email':'The e-mail must be valid.',
    }
        error_messages = {
        'username':{
            'required': 'This field must not be empty'
        }
    }
        widgets = {
        'first_name':forms.TextInput(attrs={'placeholder':'Type your username here'}),
        'password': forms.PasswordInput()
    }
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        
        if 'Lelouch' in data:
            raise ValidationError(
                'Não digite %(value)s nesse campo',
                code = 'invalid',
                params={'value':'"Lelouch"'}
            )
        return data
    
    def clean_email(self):
        data = self.cleaned_data.get('email','')
        exists = User.objects.filter(email=data).exists()
        if exists:
            raise ValidationError('O email já está em uso', code='invalid',)
        return data


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            password_confirmation_error = ValidationError(
                'Passwords dont match',
                code='invalid'
            )
            raise ValidationError({
                'password':password_confirmation_error,
                'password2':[password_confirmation_error, 'ta errado aí tio'],
            }
            )