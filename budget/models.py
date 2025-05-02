from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'user')
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    month = models.DateField()  # We'll store the first day of the month
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category', 'month')

    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.month.strftime('%B %Y')})"

    @property
    def spent_amount(self):
        """Calculate the total expenses for this budget's category in the budget's month"""
        from django.db.models import Q
        from datetime import datetime

        # Get the first and last day of the budget's month
        first_day = self.month
        if first_day.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1)

        # Calculate total expenses for this category in this month
        expenses = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            date__gte=first_day,
            date__lt=last_day
        ).aggregate(total=Sum('amount'))['total'] or 0

        return expenses
