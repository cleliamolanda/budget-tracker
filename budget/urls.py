from django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    # Transaction URLs
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/update/', views.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),

    # Budget URLs
    path('budgets/', views.BudgetListView.as_view(), name='budget-list'),
    path('budgets/create/', views.BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/<int:pk>/update/', views.BudgetUpdateView.as_view(), name='budget-update'),
    path('budgets/<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='budget-delete'),

    path('export/', views.export_csv, name='export-csv'),
]
