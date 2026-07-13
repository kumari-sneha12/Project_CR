# DriveEase Project Documentation

## 1. Project Overview
DriveEase is a full-stack web application for online car rental management.  
It allows customers to browse vehicles, apply filters, book cars, manage bookings, and maintain profiles.  
It also provides an admin panel for managing users, fleet, bookings, payments, coupons, and customer messages.

## 2. Problem Statement
Traditional car rental workflows are often manual and time-consuming.  
This project digitizes the process with a centralized platform for:
- Car discovery and booking
- Booking and payment tracking
- Customer interaction and support
- Admin-level fleet and business operations

## 3. Objectives
- Provide a clean and responsive booking experience
- Enable secure user authentication and profile management
- Automate rental cost, tax, and coupon discount calculations
- Offer booking lifecycle handling (confirm/cancel/history)
- Support operational control through a custom admin dashboard

## 4. Technology Stack
- **Backend:** Python, Django
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **UI Framework:** Bootstrap
- **Image Handling:** Pillow
- **DB Connector:** PyMySQL

## 5. System Architecture
DriveEase follows Django’s MVT pattern:
- **Models:** Data structures for users, cars, bookings, payments, coupons, wishlist, reviews, testimonials, and contact messages
- **Views:** Business logic and request handling (auth, cars, booking, admin)
- **Templates:** UI pages for customer flows, dashboard, and admin tools

## 6. Core Modules

### 6.1 Authentication & User Management
- User signup with password strength validation
- Login using username or email
- Password change and simulated reset flow
- Profile editing (avatar, bio, contact details)

### 6.2 Car Catalog
- Car listing with pagination
- Search and filtering by brand, category, price, transmission, fuel type, and seats
- Car detail page with gallery, reviews, and related cars
- Auto-complete search suggestions API

### 6.3 Wishlist
- Logged-in users can add/remove cars from wishlist
- Wishlist status is reflected in listing/details

### 6.4 Booking & Checkout
- Booking form with date/location validation
- Dynamic rental calculations:
  - rental days
  - rental cost
  - tax amount
  - coupon discount
  - grand total
- Mock payment options (Card, PayPal, Cash)
- Booking confirmation with invoice-style summary
- Booking cancellation with automatic car re-availability

### 6.5 Reviews, Testimonials & Contact
- Customers can submit car reviews and ratings
- Rating updates impact car popularity sorting
- Contact form saves support messages to database
- Testimonials shown on home page

### 6.6 Custom Admin Panel
- Dashboard with:
  - Revenue summary
  - Booking metrics
  - Car inventory count
  - Recent bookings/messages
  - Chart data (revenue trend and booking status distribution)
- Generic CRUD management for key models:
  - Users, Cars, Brands, Categories
  - Bookings, Payments, Coupons
  - Contact messages, Testimonials

## 7. Database Design (Main Entities)
- **User** (custom Django user)
- **Brand**
- **Category**
- **Car**
- **CarImage**
- **Coupon**
- **Booking**
- **Payment**
- **Wishlist**
- **Review**
- **ContactMessage**
- **Testimonial**

## 8. Main User Flow
1. User signs up / logs in  
2. User browses and filters available cars  
3. User checks car details and selects rental dates  
4. System calculates pricing and applies coupon if valid  
5. User submits booking and payment  
6. Booking confirmation and receipt are generated  
7. User can view/cancel bookings from dashboard  

## 9. Installation and Setup
1. Create and activate virtual environment  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure MySQL database (default in settings: `driveease_db`)
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. (Optional) Populate sample data:
   ```bash
   python populate_db.py
   ```
6. Start server:
   ```bash
   python manage.py runserver
   ```
7. Open:
   `http://127.0.0.1:8000/`

## 10. Preloaded Demo Data (Optional)
The `populate_db.py` script creates:
- Admin and customer demo users
- Brands, categories, premium cars
- Coupons, testimonials, and sample contact messages

## 11. Security and Validation Highlights
- Password validation checks length/complexity
- Booking date validation prevents invalid rental periods
- Coupon validation checks active state and validity window
- Server-side re-calculation prevents front-end price tampering
- Protected routes use login/staff checks

## 12. Limitations
- Payment gateway is mocked (no real transaction integration)
- Password reset is simulated (no real email service)
- `DEBUG=True` and broad host allowance are for development/demo only

## 13. Future Enhancements
- Integrate real payment gateway (Razorpay/Stripe/PayPal API)
- Real email/SMS notifications for booking and reset actions
- Availability calendar and overlap prevention
- Advanced reports and downloadable invoices
- REST API/mobile app integration

## 14. Conclusion
DriveEase demonstrates a complete end-to-end web rental platform built with Django.  
It includes customer-facing booking workflows, operational admin controls, and structured data modeling, making it suitable as a final-year college project submission.
