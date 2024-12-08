# Django E-commerce Shop

A modern e-commerce platform built with Django, featuring product management, shopping cart, and secure checkout with Stripe integration.

## Features
- Product catalog with categories
- Shopping cart functionality
- User authentication and profiles
- Admin dashboard
- Secure payments with Stripe
- Order management system

## Project Structure

### Applications

#### 1. Products App (`products/`)
- Product catalog management
- Category organization
- Product search functionality
- Features:
  - Product listing with pagination
  - Product detail views
  - Category filtering
  - Search by name and description
  - Image handling for products

#### 2. Cart App (`cart/`)
- Shopping cart management
- Session-based cart storage
- Features:
  - Add/remove products
  - Update quantities
  - Calculate totals
  - Persistent cart across sessions

#### 3. Orders App (`orders/`)
- Order processing and management
- Features:
  - Order creation
  - Order history
  - Order status tracking
  - Email notifications
  - Billing information management

#### 4. Users App (`users/`)
- Custom user authentication
- User profile management
- Features:
  - Custom user model
  - User registration
  - Profile management
  - Order history access
  - Address management

#### 5. Payment App (`payment/`)
- Stripe payment integration
- Secure payment processing
- Features:
  - Credit card processing
  - Payment verification
  - Success/failure handling
  - Test mode support
  - Webhook integration

### Core Components

#### Templates
- Base template with common elements
- Product listing and detail templates
- Cart and checkout templates
- Order management templates
- Payment processing templates

#### Static Files
- CSS stylesheets
- JavaScript files
- Images and icons
- Bootstrap integration
- Font Awesome icons

## Screenshots

### Login Page
![Login Page](screenshots/login.png)
*User login interface with clean design*

### Registration Page
![Registration Page](screenshots/register.png)
*New user registration with form validation*

### Product Listing
![Product Listing](screenshots/products.png)
*Product catalog with categories and search functionality*

### Product Detail
![Product Detail](screenshots/product-detail.png)
*Detailed product view with add to cart option*

### Shopping Cart
![Shopping Cart](screenshots/cart.png)
*Shopping cart with quantity management*

### Checkout
![Checkout](screenshots/checkout.png)
*Secure checkout process with billing information*

### Order Summary
![Order Summary](screenshots/order-summary.png)
*Order summary page showing order details and total amount*

### Payment Processing
![Payment Processing](screenshots/payment-process.png)
*Secure payment processing with Stripe integration*

### Payment Success
![Payment Success](screenshots/payment-success.png)
*Payment confirmation page after successful transaction*

### Admin Interface
![Admin Interface](screenshots/admin.png)
*Django admin interface for managing products, orders, and users*

### Admin Login
![Admin Login](screenshots/admin-login.png)
*Secure admin login interface*

## Setup Instructions
1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add:
   ```
   STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_API_VERSION=2023-10-16
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

Visit http://localhost:8000 to view the shop.
Admin interface is available at http://localhost:8000/admin

## Development

### Requirements
- Python 3.12+
- Django 5.0
- Stripe Python SDK
- Other dependencies listed in requirements.txt

### Database
- SQLite3 (default)
- Can be configured to use PostgreSQL or MySQL

### Testing
```bash
python manage.py test
```

### Security Features
- CSRF protection
- Session security
- Secure password hashing
- XSS protection
- Secure payment processing

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Django framework
- Stripe payment processing
- Bootstrap for UI components
- Font Awesome for icons
