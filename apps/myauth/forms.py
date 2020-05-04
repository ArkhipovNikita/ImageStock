from django import forms
from django.contrib.auth.forms import PasswordResetForm as PasswordResetCore, AuthenticationForm, UsernameField, \
    UserCreationForm
from django.forms import EmailField
import settings
from .models import Consumer, Author
from .tasks import send_mail


class PasswordResetForm(PasswordResetCore):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        send_mail.delay(subject_template_name=subject_template_name,
                        email_template_name=email_template_name,
                        context=context, from_email=settings.EMAIL_HOST_USER, to_email=to_email,
                        html_email_template_name=html_email_template_name)


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class RegistrationConsumerForm(UserCreationForm):
    class Meta:
        model = Consumer
        fields = ('email', 'username',)
        field_classes = {'username': UsernameField, 'email': EmailField}


class RegistrationAuthorForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ('email', 'username', 'first_name', 'last_name',)
        field_classes = {'username': UsernameField, 'email': EmailField}
