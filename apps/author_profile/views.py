from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from apps.myauth.models import Author, Consumer


class AuthorDetailMixin(SingleObjectMixin):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Author.objects.all())
        return super(AuthorDetailMixin, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailMixin, self).get_context_data(**kwargs)
        author = self.object
        is_owner = self.request.user.id == author.id
        is_followed = False
        if not is_owner:
            try:
                Consumer.objects.get(id=self.request.user.id, subscriptions__on_whom__id=author.id)
                is_followed = True
            except Exception as ex:
                pass
        context.update({
            'author': author,
            'subscribers_amount': self.object.subscribers.count(),
            'is_owner': is_owner,
            'is_followed': is_followed,
        })
        return context


@method_decorator(permission_required('myauth.view_author'), name='dispatch')
class AuthorDetailImageListView(AuthorDetailMixin, ListView):
    template_name = 'author_detail_image_list.html'
    paginate_by = 2
    ordering = ['-created_at']
    extra_context = {'section': 'images'}

    def get_queryset(self):
        self.queryset = self.object.images.order_by(*self.ordering)
        return self.queryset


@method_decorator(permission_required('myauth.view_author'), name='dispatch')
class AuthorDetailCollectionListView(AuthorDetailMixin, ListView):
    template_name = 'author_detail_collection_list.html'
    paginate_by = 2
    ordering = ['-changed_at']
    extra_context = {'section': 'collections'}

    def get_queryset(self):
        self.queryset = self.object.collections.order_by(*self.ordering)
        return self.queryset


@method_decorator(permission_required('myauth.change_author'), name='dispatch')
class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ('username', 'first_name', 'last_name', 'avatar',)
    template_name = 'author_update.html'
    extra_context = {'title': 'Update info'}

    def get_form(self, form_class=None):
        form = super(AuthorUpdateView, self).get_form()
        form.fields['avatar'].required = False
        return form

    def get_success_url(self):
        return reverse('author_detail_image', args=[self.request.user.pk])
