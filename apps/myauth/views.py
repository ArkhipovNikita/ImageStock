from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView as PasswordResetViewCore, LoginView as LoginViewCore
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from apps.myauth.forms import RegistrationAuthorForm, RegistrationConsumerForm, PasswordResetForm, LoginForm


def get_authed_user_redirect_url(request):
    user = request.user
    if user.groups.filter(name='Authors').exists():
        return reverse('author_detail_image', args=[user.id])
    else:
        return reverse('consumer_news', args=[user.id])


class RegistrationBaseView(CreateView):
    success_url = '/account/login/'
    template_name = 'registration.html'
    extra_context = {'title': 'Registration'}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(get_authed_user_redirect_url(request))
        return super(RegistrationBaseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_url'] = self.form_url
        return context

    def get_success_url(self):
        group = Group.objects.get(name=self.group)
        group.user_set.add(self.object)
        return super(RegistrationBaseView, self).get_success_url()


class RegistrationAuthorView(RegistrationBaseView):
    form_class = RegistrationAuthorForm
    form_url = 'registration_author'
    group = 'Authors'


class RegistrationConsumerView(RegistrationBaseView):
    form_class = RegistrationConsumerForm
    form_url = 'registration_consumer'
    group = 'Consumers'


class RegistrationChoiceView(TemplateView):
    template_name = 'registration_choice.html'
    extra_context = {'title': 'Select below the type of account you want to create'}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(get_authed_user_redirect_url(request))
        return super(RegistrationChoiceView, self).dispatch(request, *args, **kwargs)


class PasswordResetView(PasswordResetViewCore):
    template_name = 'password_reset.html'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.user.is_authenticated and request.user.email != form['email'].value():
            form.add_error('email', 'Please enter your email')
            return self.form_invalid(form)
        return super(PasswordResetView, self).post(request, *args, **kwargs)


class LoginView(LoginViewCore):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return get_authed_user_redirect_url(self.request)
