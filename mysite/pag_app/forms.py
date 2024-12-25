from django import forms

class DataForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': '2007-01-01', 'max': '2015-12-31'}), 
                           required=False)
    data_type = forms.ChoiceField(choices=[('month', 'Month'), ('year', 'Year')], required=False)