from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from apps.myauth.models import Author
from apps.subscription_handling.models import Subscription
from django.shortcuts import get_object_or_404


@method_decorator(permission_required('subscription_handling.add_subscription'), name='dispatch')
class SubscriptionView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        consumer = request.user
        author_pk = kwargs['pk']
        author = get_object_or_404(Author, pk=author_pk)
        Subscription.objects.create(who_id=consumer.id, on_whom_id=author.id)
        return HttpResponseRedirect('/account/author/%s' % author_pk)


@method_decorator(permission_required('subscription_handling.delete_subscription'), name='dispatch')
class UnsubscriptionView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        consumer = request.user
        author_pk = kwargs['pk']
        author = get_object_or_404(Author, pk=author_pk)
        Subscription.objects.get(who_id=consumer.id, on_whom_id=author.id).delete()
        return HttpResponseRedirect('/account/author/%s' % author_pk)
