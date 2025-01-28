from django import forms

class DataForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'month',
                'min': '2014-01',
                'max': '2018-12',
                'class': 'form-control'
            },
            format='%Y-%m'
        ),
        input_formats=['%Y-%m'],
        required=False
    )