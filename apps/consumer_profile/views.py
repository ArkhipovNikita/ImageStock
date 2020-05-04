from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from apps.image_handling.models import Image
from apps.myauth.models import Consumer


@method_decorator(permission_required('myauth.view_consumer'), name='dispatch')
class ConsumerNewsView(LoginRequiredMixin, SingleObjectMixin, ListView):
    model = Image
    template_name = 'consumer_news.html'
    paginate_by = 3
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Consumer.objects.all())
        return super(ConsumerNewsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConsumerNewsView, self).get_context_data(**kwargs)
        context.update({
            'consumer': self.object,
        })
        return context

    def get_queryset(self):
        return self.model.objects.filter(author_id__in=self.object.subscriptions.values_list('on_whom', flat=True))


@method_decorator(permission_required('myauth.change_consumer'), name='dispatch')
class ConsumerUpdateView(UpdateView, LoginRequiredMixin):
    model = Consumer
    fields = ('username', 'avatar',)
    template_name = 'consumer_update.html'
    extra_context = {'title': 'Update info'}

    def get_form(self, form_class=None):
        form = super(ConsumerUpdateView, self).get_form()
        form.fields['avatar'].required = False
        return form

    def get_success_url(self):
        return reverse('consumer_news', args=[self.request.user.id])
