from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware
from .models import Category, Transaction, Budget
from .forms import CategoryForm, TransactionForm, BudgetForm, UserRegisterForm, ExportFilterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import csv
from django.http import HttpResponse

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
    success_url = reverse_lazy('budget:budget-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        context['submit_text'] = 'Create'
        context['cancel_url'] = reverse_lazy('budget:budget-list')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            inputted_category = form.cleaned_data.get('name')
            form.add_error('name', f"The category {inputted_category} already exists.")
            return self.form_invalid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'budget/form.html'
    success_url = reverse_lazy('budget:budget-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Category'
        context['submit_text'] = 'Update'
        context['cancel_url'] = reverse_lazy('budget:budget-list')
        return context

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'budget/confirm_delete.html'
    success_url = reverse_lazy('budget:budget-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('budget:budget-list')
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
        month_filter = self.request.GET.get('month', None)
        category_filter = self.request.GET.get('category', None)

        queryset = Budget.objects.filter(user=self.request.user)

        if month_filter:
            try:
                selected_month = datetime.strptime(month_filter, '%Y-%m')
                queryset = queryset.filter(month__year=selected_month.year, month__month=selected_month.month)
            except ValueError:
                pass  # Invalid date format
        
        if category_filter:
            queryset = queryset.filter(category__id=category_filter)

        return queryset.order_by('month')  # Return ordered by month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Budgets'
        context['headers'] = ['Category', 'Amount', 'Month']
        context['create_url'] = 'budget:budget-create'
        context['update_url'] = 'budget:budget-update'
        context['delete_url'] = 'budget:budget-delete'
        context['categories'] = Category.objects.filter(user=self.request.user)
        
        # Add current month filter default
        current_month = datetime.now().strftime('%Y-%m')
        context['current_month'] = current_month

        # Add month filter to context
        context['month_filter'] = self.request.GET.get('month', current_month)
        context['category_filter'] = self.request.GET.get('category', None)

        return context

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget/form.html'

    def get_success_url(self):
        # Get the current month in 'YYYY-MM' format
        current_month = timezone.now().strftime('%Y-%m')
        # Redirect to the budget list page with the current month as a query parameter
        return reverse('budget:budget-list') + f'?month={current_month}'

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

    # Define the current month's date range
    today = timezone.now().date()
    current_month_first_day = today.replace(day=1)
    current_month_last_day = (current_month_first_day + relativedelta(months=1)) - timedelta(days=1)

    # Convert to datetime range (handles DateTimeField safely)
    start_of_day = make_aware(datetime.combine(current_month_first_day, datetime.min.time()))
    end_of_day = make_aware(datetime.combine(current_month_last_day, datetime.max.time()))

    # Get transactions for the current month
    current_month_transactions = Transaction.objects.filter(
        user=request.user,
        date__range=[start_of_day, end_of_day]
    )

    # Calculate current month income, expenses, and balance
    current_month_income = current_month_transactions.filter(transaction_type='income').aggregate(
        total=Sum('amount')
    )['total'] or 0

    current_month_expenses = current_month_transactions.filter(transaction_type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0

    current_month_balance = current_month_income - current_month_expenses

    # Generate data for each month of the current year
    monthly_data = []

    for month in range(1, 13):  # January to December
        month_start = datetime(today.year, month, 1).date()
        month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)

        start_of_day = make_aware(datetime.combine(month_start, datetime.min.time()))
        end_of_day = make_aware(datetime.combine(month_end, datetime.max.time()))

        month_transactions = Transaction.objects.filter(
            user=request.user,
            date__range=[start_of_day, end_of_day]
        )

        # Calculate even if empty
        month_income = month_transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0

        month_expenses = month_transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        month_balance = month_income - month_expenses
        month_name = month_start.strftime('%b %Y')

        monthly_data.append({
            'label': month_name,
            'income': float(month_income),
            'expenses': float(month_expenses),
            'balance': float(month_balance)
        })

    # Get category expenses for the current month
    category_expenses = current_month_transactions.filter(
        transaction_type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Get budgets for the current month
    budgets = Budget.objects.filter(
        user=request.user,
        month=current_month_first_day
    ).select_related('category')

    # Create a dictionary to store spent amounts per category
    budget_spent = {}

    for budget in budgets:
        category_id = budget.category.id
        spent = current_month_transactions.filter(
            transaction_type='expense',
            category_id=category_id
        ).aggregate(total=Sum('amount'))['total'] or 0.0
        budget_spent[category_id] = spent

    # Prepare chart data
    if category_expenses:
        category_names = [item['category__name'] for item in category_expenses]
        category_values = [float(item['total']) for item in category_expenses]
    else:
        category_names = []
        category_values = []

    context = {
        'income': current_month_income,
        'expenses': current_month_expenses,
        'balance': current_month_balance,
        'category_expenses': category_expenses,
        'category_names': category_names,
        'category_values': category_values,
        'budgets': budgets,
        'budget_spent': budget_spent,
        'monthly_data': monthly_data
    }

    if settings.DEBUG:
        context['debug_info'] = {
            'has_transactions': current_month_transactions.exists(),
            'transaction_count': current_month_transactions.count(),
            'has_category_expenses': bool(category_expenses),
            'has_budgets': budgets.exists(),
            'monthly_data': monthly_data
        }

    return render(request, 'budget/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def export_csv(request):
    form = ExportFilterForm(user=request.user, data=request.GET or None)
    if form.is_valid() and request.GET:
        # Filter transactions based on form data
        transactions = Transaction.objects.filter(user=request.user)
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        category = form.cleaned_data.get('category')

        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if category:  # Only filter by category if a specific category is selected
            transactions = transactions.filter(category_id=category)

        # Generate a filename with the current date and time
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"transactions_{current_time}.csv"

        # CSV response logic
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Title', 'Amount', 'Type', 'Category', 'Date', 'Notes'])
        for transaction in transactions:
            writer.writerow([
                transaction.title,
                transaction.amount,
                transaction.transaction_type,
                transaction.category.name if transaction.category else '',
                transaction.date.strftime('%Y-%m-%d'),  # Format the date
                transaction.notes,
            ])
        return response

    return render(request, 'budget/export_csv.html', {'form': form})
