from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from apps.collection_handling.models import Collection
from apps.image_handling.models import Image


@method_decorator(permission_required('collection_handling.add_collection'), name='dispatch')
class CollectionCreateView(CreateView, LoginRequiredMixin):
    model = Collection
    fields = ('name', 'cover', 'images',)
    template_name = 'collection_create.html'
    extra_context = {'title': 'Collection creation'}

    def get_form(self, form_class=None):
        form = super(CollectionCreateView, self).get_form(form_class)
        form.fields['images'].required = False
        form.fields['cover'].required = False
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author_id = self.request.user.id
        images = form.cleaned_data['images']
        instance.save()
        instance.images.set(images)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('author_detail_collection', args=[self.request.user.id])


@method_decorator(permission_required('collection_handling.view_collection'), name='dispatch')
class CollectionDetailView(SingleObjectMixin, ListView):
    model = Image
    template_name = 'collection_detail.html'
    paginate_by = 2
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Collection.objects.all())
        return super(CollectionDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)
        context.update({
            'collection': self.object,
        })
        return context

    def get_queryset(self):
        self.queryset = self.object.images.order_by(*self.ordering)
        return self.queryset


@method_decorator(permission_required('collection_handling.change_collection'), name='dispatch')
class CollectionUpdateView(UpdateView, LoginRequiredMixin):
    model = Collection
    fields = ('name', 'cover', 'images', )
    template_name = 'collection_update.html'
    extra_context = {'title': 'Collection update'}

    def get_form(self, form_class=None):
        form = super(CollectionUpdateView, self).get_form()
        form.fields['images'].required = False
        return form

    def get_success_url(self):
        return reverse('collection_detail', args=[self.kwargs['pk']])


@method_decorator(permission_required('collection_handling.delete_collection'), name='dispatch')
class CollectionDeleteView(DeleteView, LoginRequiredMixin):
    model = Collection

    def get_success_url(self):
        return reverse('author_detail_collection', args=[self.request.user.id])
