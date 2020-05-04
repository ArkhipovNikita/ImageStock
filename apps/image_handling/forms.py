from django import forms
from django.core.exceptions import ValidationError

from apps.collection_handling.models import Collection
from apps.image_handling.models import Image, Tag
import re


def validate_comma_separated_list(value):
    pattern = '[\\dа-яА-ЯёЁ]+'
    if re.search(pattern, value):
        raise ValidationError('Tags field contains non-Latin letters or digits')
    pattern = '[^,0-9a-zA-Z]+'
    if re.search(pattern, value):
        raise ValidationError('Tags field contains prohibited symbols')
    if len(value.split(',')) < 2:
        raise ValidationError('Tags field contains to less tags')


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('name', 'original', 'price', 'category', 'collections', 'description')
        labels = {
            'original': 'Image',
            'price': 'Image price in $'
        }

    tags = forms.CharField(widget=forms.Textarea,
                           label='Tags',
                           help_text='Enter at least 2 tags in English separated with comma',
                           validators=[validate_comma_separated_list],)
    collections = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ImageCreateForm, self).__init__(*args, **kwargs)
        self.fields['collections'].queryset = Collection.objects.filter(author_id=user.id)

    def _clean_fields(self):
        super(ImageCreateForm, self)._clean_fields()
        if not self._errors:
            self.cleaned_data['tags'] = self.cleaned_data['tags'].split(',')


class ImageUpdateForm(ImageCreateForm):
    class Meta:
        model = Image
        fields = ('name', 'price', 'category', 'collections', 'tags', 'description')
        labels = {
            'price': 'Image price in $'
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        image_id = kwargs['instance'].id
        tags = Tag.objects.filter(image__id=image_id)
        initial['tags'] = ','.join([tag.name for tag in tags])
        kwargs.update(initial=initial)
        super(ImageUpdateForm, self).__init__(*args, **kwargs)
