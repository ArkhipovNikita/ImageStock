from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView
from django.shortcuts import get_object_or_404

from apps.image_handling.models import Image
from apps.purchase_handling.models import Purchase


@method_decorator(permission_required('purchase_handling.view_purchase'), name='dispatch')
class PurchaseListView(ListView, LoginRequiredMixin):
    model = Purchase
    paginate_by = 5
    template_name = 'purchases_list.html'
    extra_context = {'title': 'Your purchases'}
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Authors').exists():
            return Purchase.objects.filter(seller_id=user.id).select_related('image').order_by(*self.ordering)
        else:
            return Purchase.objects.filter(buyer_id=user.id).select_related('image').order_by(*self.ordering)


@method_decorator(permission_required('purchase_handling.view_purchase'), name='dispatch')
class PurchaseCreateView(TemplateView, LoginRequiredMixin):
    template_name = 'purchase_create.html'
    extra_context = {'title': 'Buying an image'}

    def post(self, request, *args, **kwargs):
        subject_of_bargain = get_object_or_404(Image.objects.select_related('author'), pk=self.kwargs['pk'])
        Purchase.objects.create(
            buyer_id=self.request.user.id,
            seller_id=subject_of_bargain.author.id,
            image_id=subject_of_bargain.id)
        subject_of_bargain.purchase_count = F('purchase_count') + 1
        subject_of_bargain.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(PurchaseCreateView, self).get_context_data(**kwargs)
        image = get_object_or_404(Image, pk=kwargs['pk'])
        context.update({
            'image_id': image.id
        })
        return context

    def get_success_url(self):
        return reverse('image_detail', args=[self.kwargs['pk']])
