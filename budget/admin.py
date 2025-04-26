from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'category', 'user', 'date')
    list_filter = ('transaction_type', 'category', 'user', 'date')
    search_fields = ('title', 'notes', 'user__username')
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'month', 'user')
    list_filter = ('category', 'user', 'month')
    search_fields = ('category__name', 'user__username')
    date_hierarchy = 'month'
