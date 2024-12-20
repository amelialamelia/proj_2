from django import forms

class DataForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    data_type = forms.ChoiceField(choices=[('day', 'Day'), ('month', 'Month'), ('year', 'Year')], required=False)