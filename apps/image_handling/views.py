from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from .forms import *
from .models import Tag
from ..purchase_handling.models import Purchase


class ImageBaseFormView:
    def form_valid(self, form):
        tags = form.cleaned_data['tags']
        Tag.objects.bulk_create([Tag(name=tag) for tag in tags], ignore_conflicts=True)
        tags = Tag.objects.in_bulk(tags, field_name='name')
        obj = form.save(commit=False)
        obj.author_id = self.request.user.id
        obj.save()
        obj.collections.set(form.cleaned_data['collections'])
        obj.tags.add(*[tag.id for tag in tags.values()])
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


@method_decorator(permission_required('image_handling.add_image'), name='dispatch')
class ImageCreateFormView(ImageBaseFormView, CreateView, LoginRequiredMixin):
    form_class = ImageCreateForm
    template_name = 'image_upload.html'
    extra_context = {'title': 'Image upload'}

    def get_success_url(self):
        return reverse('author_detail_image', args=[self.request.user.id])


@method_decorator(permission_required('image_handling.change_image'), name='dispatch')
class ImageUpdateFormView(ImageBaseFormView, UpdateView, LoginRequiredMixin):
    model = Image
    form_class = ImageUpdateForm
    template_name = 'image_update.html'
    extra_context = {'title': 'Image update'}

    def get_success_url(self):
        return reverse('image_detail', args=[self.kwargs['pk']])


# @method_decorator(permission_required('image_handling.view_image'), name='dispatch')
class ImageDetailView(DetailView):
    model = Image
    template_name = 'image_detail.html'
    extra_context = {'title': 'Image view'}

    def get_context_data(self, **kwargs):
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        is_owner = self.object.author.id == self.request.user.id
        is_bought = False
        if not is_owner:
            is_bought = Purchase.objects.select_related('image_id')\
                .filter(buyer_id=self.request.user.id, image_id=self.kwargs['pk']).exists()
        context.update({
            'is_bought': is_bought,
        })
        return context


@method_decorator(permission_required('image_handling.delete_image'), name='dispatch')
class ImageDeleteView(DeleteView, LoginRequiredMixin):
    model = Image

    def get_success_url(self):
        return reverse('author_detail_image', args=[self.request.user.id])
