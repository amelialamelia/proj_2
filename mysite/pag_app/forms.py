from django import forms

class DataForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': '2014-01-01', 'max': '2018-12-31'}), 
                           required=False)