from django import forms
from django.forms import inlineformset_factory
from .models import FarmReport, Expense, Income

class FarmReportForm(forms.ModelForm):
    class Meta:
        model = FarmReport
        fields = '__all__'
        widgets = {
            'date_of_sowing': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_harvest': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'farmer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'crop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'season': forms.Select(attrs={'class': 'form-select'}),
            'total_acres': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
        }

ExpenseFormSet = inlineformset_factory(
    FarmReport, Expense, form=ExpenseForm, extra=1, can_delete=True
)
IncomeFormSet = inlineformset_factory(
    FarmReport, Income, form=IncomeForm, extra=1, can_delete=True
)
