__author__ = 'keyvan'

from django import forms


class SubmitSentenceForm(forms.Form):
    type_in_a_sentence = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'cols': 50,
                'placeholder': 'Type in a sentence here',
            }
        ),
    )

    language = forms.ChoiceField(
        required=True,
        choices=(
            ('en', 'English'),
            ('ru', 'Russian'),
            ('de', 'German')
        ),
        widget=forms.Select(
            attrs={
                'onchange': 'language_changed()',
            }
        ),
        initial='all')

    choose_version = forms.ChoiceField(
        choices=(
            ('rel', 'Latest release version'),
            ('dev', 'Alternate development version'),
        ),
        initial='all')