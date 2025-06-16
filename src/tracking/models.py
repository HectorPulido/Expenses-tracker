from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Expense(models.Model):
    TYPE_CHOICES = [
        ("0", "Expense"),
        ("1", "Income"),
    ]
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type_data = models.CharField(max_length=1, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    date_reg = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_data}: {self.description} (${self.value})"
