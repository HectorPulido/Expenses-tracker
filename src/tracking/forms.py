from django import forms
from django.contrib.auth.models import User
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label="Category",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
                "size": "5",
            }
        ),
    )

    class Meta:
        model = Expense
        fields = [
            "type_data",
            "periodicity",
            "description",
            "value",
            "issue_date",
            "categories",
        ]
        widgets = {
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description",
                }
            ),
            "type_data": forms.Select(attrs={"class": "form-select"}),
            "periodicity": forms.Select(attrs={"class": "form-select"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "issue_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["categories"].queryset = Category.objects.filter(user=user)


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
