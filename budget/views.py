from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Transaction, Budget
from .forms import CategoryForm, TransactionForm, BudgetForm

# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'budget/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categories'
        context['headers'] = ['Name', 'Created At', 'Updated At']
        context['create_url'] = 'budget:category-create'
        context['update_url'] = 'budget:category-update'
        context['delete_url'] = 'budget:category-delete'
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        context['submit_text'] = 'Create'
        context['cancel_url'] = reverse_lazy('budget:category-list')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Category'
        context['submit_text'] = 'Update'
        context['cancel_url'] = reverse_lazy('budget:category-list')
        return context

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'budget/confirm_delete.html'
    success_url = reverse_lazy('budget:category-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('budget:category-list')
        return context

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'budget/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Transactions'
        context['headers'] = ['Title', 'Amount', 'Type', 'Category', 'Date']
        context['create_url'] = 'budget:transaction-create'
        context['update_url'] = 'budget:transaction-update'
        context['delete_url'] = 'budget:transaction-delete'
        return context

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Transaction'
        context['submit_text'] = 'Create'
        context['cancel_url'] = reverse_lazy('budget:transaction-list')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Transaction'
        context['submit_text'] = 'Update'
        context['cancel_url'] = reverse_lazy('budget:transaction-list')
        return context

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'budget/confirm_delete.html'
    success_url = reverse_lazy('budget:transaction-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('budget:transaction-list')
        return context

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budget/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Budgets'
        context['headers'] = ['Category', 'Amount', 'Month']
        context['create_url'] = 'budget:budget-create'
        context['update_url'] = 'budget:budget-update'
        context['delete_url'] = 'budget:budget-delete'
        return context

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:budget-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Budget'
        context['submit_text'] = 'Create'
        context['cancel_url'] = reverse_lazy('budget:budget-list')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:budget-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Budget'
        context['submit_text'] = 'Update'
        context['cancel_url'] = reverse_lazy('budget:budget-list')
        return context

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budget/confirm_delete.html'
    success_url = reverse_lazy('budget:budget-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('budget:budget-list')
        return context

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    today = timezone.now().date()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[first_day, last_day]
    )

    income = transactions.filter(transaction_type='income').aggregate(
        total=Sum('amount')
    )['total'] or 0

    expenses = transactions.filter(transaction_type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0

    category_expenses = transactions.filter(
        transaction_type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    )

    budgets = Budget.objects.filter(
        user=request.user,
        month=first_day
    )

    context = {
        'income': income,
        'expenses': expenses,
        'balance': income - expenses,
        'category_expenses': category_expenses,
        'budgets': budgets
    }

    return render(request, 'budget/dashboard.html', context)
