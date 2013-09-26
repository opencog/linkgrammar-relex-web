__author__ = 'keyvan'

from django import forms


class SubmitSentenceForm(forms.Form):
    type_in_a_sentence = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Type in a sentence here',
            }
        ),
    )

    language = forms.ChoiceField(
        required=True,
        choices=(
            ('en', 'English'),
            ('ru', 'Russian')
        ),
        widget=forms.RadioSelect()
    )

    choose_version = forms.ChoiceField(
        choices=(
            ('rel', 'Latest release version'),
            ('dev', 'Alternate development version'),
        ),
        widget=forms.RadioSelect()
    )