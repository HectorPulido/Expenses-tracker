from django.contrib import admin
from .models import Expense, Category


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
