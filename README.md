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
![{E0C5B078-BA10-4E67-B472-70047DDC5C85}](https://github.com/user-attachments/assets/4ccde7c1-2266-4b06-ac56-e7694e1c9c98)

*User login interface with clean design*

### Registration Page
![{C0DAE3D1-DE4B-4D34-9BEC-8CA9F6868574}](https://github.com/user-attachments/assets/27e603f9-42b6-4b1e-a996-9cdd81070ccc)

*New user registration with form validation*

### Product Listing
![{1A9B5A8E-A228-480D-8ECE-69B6A2E946F7}](https://github.com/user-attachments/assets/d324ae3b-99f4-4b3c-9d15-94319a84967d)

*Product catalog with categories and search functionality*

### Product Detail
![{348853DD-AB40-4398-9222-17551B4517D9}](https://github.com/user-attachments/assets/ed79d188-9a9b-4ec1-9a8c-bbb606fa45a6)

*Detailed product view with add to cart option*

### Shopping Cart
![{C6524670-0CF5-4F2C-9A99-F757ABF9A34E}](https://github.com/user-attachments/assets/0e20ab73-0bee-41ec-80d2-9444a622ea1b)

*Shopping cart with quantity management*

### Checkout
![{5ED5C0F0-724F-4DFC-8264-BC75B3DC8924}](https://github.com/user-attachments/assets/e28914f0-b8ea-499d-aafa-b654cd0d83ab)

*Secure checkout process with billing information*

### Order Summary
![{1EA436F2-3858-4D2A-BDBD-73688178145D}](https://github.com/user-attachments/assets/fb23775f-0c8e-40c6-93b2-702f42410457)

*Order summary page showing order details and total amount*

### Payment Processing
![{DE4FF501-6C3C-4022-970B-4055586FBFAE}](https://github.com/user-attachments/assets/87464748-dfe9-44e6-ac84-a1c14a8c8a5e)

*Secure payment processing with Stripe integration*

### Payment Success
![{C16E33B7-7114-499E-A037-18BA21EA44A2}](https://github.com/user-attachments/assets/4cf90d1b-30ca-4a1b-8346-b4eab9440f91)

*Payment confirmation page after successful transaction*

### Admin Interface
![{43EBF634-8A47-4442-BD95-21ADBFB36F1F}](https://github.com/user-attachments/assets/41e8aad6-7937-43d8-b446-ac5b7bd019bd)

*Django admin interface for managing products, orders, and users*

### Admin Login
![{506D57B9-BF13-43FD-B75F-5A318ACBDF5C}](https://github.com/user-attachments/assets/73e9e75a-46a4-4096-b05a-1bd0a19cad5d)

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
