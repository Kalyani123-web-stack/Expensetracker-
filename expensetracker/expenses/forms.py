from django import forms
from .models import Expense
from .models import Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        fields=['amount','description','category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']