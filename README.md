# Budget Co. Backend

A Django REST framework backend for a personal budget tracking application.

## Features

- User authentication with JWT
- CRUD operations for categories, transactions, and budgets
- Monthly financial summaries
- Category-based expense tracking
- Budget setting and monitoring

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Transactions
- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create a new transaction
- `GET /api/transactions/{id}/` - Get transaction details
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/transactions/monthly_summary/` - Get monthly summary
- `GET /api/transactions/category_summary/` - Get category-wise summary

### Budgets
- `GET /api/budgets/` - List all budgets
- `POST /api/budgets/` - Create a new budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget
- `GET /api/budgets/current_month/` - Get current month's budgets

## Authentication

All endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Development

To run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Team Contributions

### Randall
- Set up the workspace environment
- Designed navigation bar
- Designed general layout of the **Budgets List**
- Ensured application responsiveness across devices
- Ensured app reactivity (dynamic updates and state handling)

### Clay
- UI/UX Design
- Designed **Login** and **Register** pages (UI/UX)
- Created general layout for **Dashboard** and **Transactions**
- Developed consistent general styles:
  - Cards
  - Forms
  - Tables
  - Buttons
  - Icons
  - Brand logo
- Implemented export functionality for income/expense data (CSV)

### Jade
- Developed analytics visualizations (charts)
- Ensured correct currency formatting and human-readable date display
- Added accessibility features (ARIA labels)

### All Members
- Collaborated to improve overall code quality
