from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from apps.board_handling.models import Board
from apps.image_handling.models import Image


@method_decorator(permission_required('board_handling.add_board'), name='dispatch')
class BoardCreateView(CreateView, LoginRequiredMixin):
    model = Board
    fields = ('name', 'images',)
    template_name = 'board_create.html'
    extra_context = {'title': 'Board creation'}

    def get_form(self, form_class=None):
        form = super(BoardCreateView, self).get_form()
        form.fields['images'].required = False
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner_id = self.request.user.id
        images = form.cleaned_data['images']
        instance.save()
        instance.images.set(images)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('board_list')


@method_decorator(permission_required('board_handling.view_board'), name='dispatch')
class BoardDetailView(SingleObjectMixin, ListView):
    model = Image
    template_name = 'board_detail.html'
    paginate_by = 3
    ordering = ['-created_at']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Board.objects.all())
        return super(BoardDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoardDetailView, self).get_context_data(**kwargs)
        context.update({
            'board': self.object,
        })
        return context

    def get_queryset(self):
        self.queryset = self.object.images.order_by(*self.ordering)
        return self.queryset


@method_decorator(permission_required('board_handling.view_board'), name='dispatch')
class BoardListView(ListView, LoginRequiredMixin):
    model = Board
    template_name = 'board_list.html'
    paginate_by = 3
    ordering = ['-created_at']

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.id)


@method_decorator(permission_required('board_handling.change_board'), name='dispatch')
class BoardUpdateView(UpdateView, LoginRequiredMixin):
    model = Board
    fields = ('name', 'images',)
    template_name = 'board_update.html'
    extra_context = {'title': 'Board update'}

    def get_form(self, form_class=None):
        form = super(BoardUpdateView, self).get_form()
        form.fields['images'].required = False
        return form

    def get_success_url(self):
        return reverse('board_detail', args=[self.kwargs['pk']])


@method_decorator(permission_required('board_handling.delete_board'), name='dispatch')
class BoardDeleteView(DeleteView, LoginRequiredMixin):
    model = Board

    def get_success_url(self):
        return reverse('board_list')
