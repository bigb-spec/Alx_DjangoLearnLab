# bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label="Book Title")
    author = forms.CharField(max_length=100, required=True, label="Author")
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False, 
        label="Published Date"
    )