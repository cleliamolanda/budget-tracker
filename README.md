# Budget Co. Backend

A Django framework backend for a personal budget tracking application.

---

## Features

- **User Authentication**: Secure login and token-based authentication using JWT.
- **Budget Management**: Create, update, and monitor budgets.
- **Transaction Tracking**: Record and categorize expenses and income.
- **Monthly Summaries**: View financial summaries for the current month.
- **Category Insights**: Analyze expenses by category.

- **User Dashboard**: View budgets, transactions, and summaries.
- **Interactive Charts**: Visualize spending trends and category insights.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Real-Time Updates**: Reflect changes in budgets and transactions instantly.

---

## Setup Instructions

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Dallss/budget-tracker.git
   cd budget-tracker
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

   The API will be available at: `http://localhost:8000/api/`

---

## User Guide

### Authentication

All API endpoints require authentication using JWT tokens. Obtain a token by logging in:

- **Get JWT Token**:
  `POST /api/token/`
  Request a token by providing valid user credentials.

- **Refresh JWT Token**:
  `POST /api/token/refresh/`
  Refresh an expired token.

Include the token in the `Authorization` header for all requests:
```
Authorization: Bearer <your_token>
```

---

### API Endpoints

#### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

#### Transactions
- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create a new transaction
- `GET /api/transactions/{id}/` - Get transaction details
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/transactions/monthly_summary/` - Get monthly summary
- `GET /api/transactions/category_summary/` - Get category-wise summary

#### Budgets
- `GET /api/budgets/` - List all budgets
- `POST /api/budgets/` - Create a new budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget
- `GET /api/budgets/current_month/` - Get current month's budgets

---

## Development

To run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

# Team Contributions

## Randall
- Set up the workspace environment
- Designed navigation bar
- Designed general layout of the **Budgets List**
- Ensured application responsiveness across devices
- Ensured app reactivity (dynamic updates and state handling)

## Clay
- UI/UX Design
- Designed **Login** and **Register** pages (UI/UX)
- Created general layout for **Dashboard** and **Transactions**
- Developed consistent general styles (cards, forms, tables, buttons, brand logo)
- Implemented export functionality for income/expense data (CSV)

## Jade
- Developed analytics visualizations (charts)
- Ensured correct currency formatting and human-readable date display
- Added accessibility features (ARIA labels)

## All Members
- Collaborated to improve overall code quality and accessibility
