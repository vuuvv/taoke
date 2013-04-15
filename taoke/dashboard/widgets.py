import copy
from django import forms

class TextBox(forms.TextInput):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'input_text'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(TextBox, self).__init__(attrs=final_attrs)

