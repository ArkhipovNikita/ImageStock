from urllib.parse import urlencode

from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, ListView

from apps.image_handling.models import Image
from apps.image_searching.forms import SearchForm


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'search.html'

    def form_valid(self, form):
        q = form.cleaned_data['tags'].split(',')
        base_url = reverse('search_result')
        query_string = urlencode({'q': '+'.join(q)})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


class SearchResultView(ListView):
    model = Image
    template_name = 'search_result.html'

    def get_queryset(self):
        q = self.request.GET.get('q').split('+')
        q = [t.lower() for t in q]
        return Image.objects.filter(Q(tags__name__in=q) | Q(name__icontains=q) | Q(description__icontains=q)).distinct()
