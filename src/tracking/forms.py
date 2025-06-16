from django import forms
from django.contrib.auth.models import User
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["type_data", "value", "description", "issue_date"]


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
