from django import forms
import re

from django.core.exceptions import ValidationError


def validate_comma_separated_list(value):
    pattern = '[\\dа-яА-ЯёЁ]+'
    if re.search(pattern, value):
        raise ValidationError('Tags field contains non-Latin letters or digits')
    pattern = '[^,0-9a-zA-Z]+'
    if re.search(pattern, value):
        raise ValidationError('Tags field contains prohibited symbols')


class SearchForm(forms.Form):
    tags = forms.CharField(help_text='Enters tags separated by comma',
                           validators=[validate_comma_separated_list],
                           label='')
