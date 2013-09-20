from django.forms.models import ModelForm, BaseInlineFormSet
from parser_ui.models import Server

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
        initial='all')

    options = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ("ct", "Show constituent trees"),
            ("nl", "Allow null links"),
            ("al", "Show all linkages"),
        )
    )

    number_of_linkages_to_show = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'number',
                'onkeydown': 'validate_number(event)',
                'value': '1'
            }
        ),
        required=False,
        max_length=3,
    )

    choose_version = forms.ChoiceField(
        choices=(
            ('rel', 'Latest release version'),
            ('dev', 'Alternate development version'),
        ),
        initial='all')