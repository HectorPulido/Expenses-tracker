from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "name")
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Expense(models.Model):
    TYPE_CHOICES = [
        ("0", "Expense"),
        ("1", "Income"),
    ]
    PERIODICITY_CHOICES = [
        ("O", "One time"),
        ("R", "Recurrent"),
    ]
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type_data = models.CharField(max_length=1, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    date_reg = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(Category, blank=True, related_name="expenses")
    periodicity = models.CharField(
        max_length=1,
        choices=PERIODICITY_CHOICES,
        default="O",
        help_text="Select if recurrent payment",
    )

    def __str__(self):
        return f"{self.type_data}: {self.description} (${self.value})"
