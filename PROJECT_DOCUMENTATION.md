# DriveEase — Comprehensive Project Documentation

## 1) Executive Summary
DriveEase is a Django-based full-stack car rental platform that provides:
- Customer flows: authentication, car discovery, wishlist, booking, checkout, and booking management.
- Operations flows: custom staff dashboard, model-level CRUD tools, business metrics, and customer message management.

The system is implemented as a monolithic Django application with clear module boundaries across `models`, `views`, `forms`, `utilities`, templates, and static assets.

---

## 2) Scope and Goals
### In Scope
- User registration, login, profile management, and password update/reset simulation.
- Vehicle catalog browsing with search, filters, sorting, pagination, and suggestions API.
- Booking lifecycle with coupon support, tax/discount calculations, payment simulation, and cancellation.
- Review and testimonial support.
- Contact messaging and admin-side unread tracking.
- Custom admin panel for analytics and generic CRUD operations.

### Current Non-Goals
- Real payment gateway integration.
- Email/SMS infrastructure for password reset and booking alerts.
- Production-hardened security defaults in settings.

---

## 3) Technology Stack
- **Language:** Python 3.x
- **Framework:** Django 5.x
- **Database:** MySQL (configured in `driveease/settings.py`)
- **Image/Media:** Pillow
- **MySQL Driver:** PyMySQL
- **Frontend:** Django templates, Bootstrap, CSS, JavaScript

Dependencies (`requirements.txt`):
- `Django>=5.0,<5.2`
- `PyMySQL>=1.1.0`
- `Pillow>=10.0.0`

---

## 4) High-Level Architecture
DriveEase follows Django’s MVT architecture:
- **Models:** Domain entities for users, cars, booking/payment, and interactions.
- **Views:** Request orchestration and business flow handling.
- **Templates:** Server-rendered UI with contextual data.
- **Forms:** Input validation and model/form binding.
- **Utilities:** Shared pricing logic (`calculate_booking_details`).
- **Context Processor:** Global categories/brands/wishlist/message counters.

### Runtime Characteristics
- Monolith app (`rental`) mounted under project `driveease`.
- Mixed sync page rendering and lightweight JSON endpoints.
- Media served locally in DEBUG mode.

---

## 5) Repository and Module Structure
```text
/home/runner/work/Project_CR/Project_CR
├── driveease/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── rental/
│   ├── models/
│   │   ├── auth.py
│   │   ├── car.py
│   │   ├── booking.py
│   │   ├── interactions.py
│   │   ├── wishlist.py
│   │   └── __init__.py
│   ├── views/
│   │   ├── home.py
│   │   ├── auth.py
│   │   ├── cars.py
│   │   ├── booking.py
│   │   └── custom_admin.py
│   ├── forms/
│   │   ├── auth.py
│   │   ├── booking.py
│   │   └── contact.py
│   ├── utilities/helpers.py
│   ├── context_processors.py
│   ├── migrations/
│   └── urls.py
├── templates/
├── static/
├── media/
├── manage.py
├── populate_db.py
├── requirements.txt
└── PROJECT_DOCUMENTATION.md
```

---

## 6) Configuration and Environment
### Key Django Settings
File: `driveease/settings.py`
- `INSTALLED_APPS`: includes `rental` and default Django apps.
- `AUTH_USER_MODEL = 'rental.User'` (custom user model).
- `DATABASES`: MySQL database `driveease_db` (host `127.0.0.1`, port `3306`, user `root`, empty password by default).
- `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_ROOT`, `MEDIA_URL` configured.
- `DEBUG=True`, `ALLOWED_HOSTS=['*']` (development setup).

### URL Wiring
- Project root routes: `driveease/urls.py`
  - `/admin/` → Django admin
  - `/` → includes `rental.urls`

---

## 7) Domain Model (Complete)

### 7.1 User (`rental.models.auth.User`)
Extends `AbstractUser`.
- Additional fields: `phone`, `avatar`, `bio`, `is_customer`, `is_staff_admin`.
- Role logic in app checks `is_staff`, `is_staff_admin`, `is_superuser` for custom admin access.

### 7.2 Brand (`rental.models.car.Brand`)
- Fields: `name`, `slug`, `logo`.
- Behavior: auto-generates slug from name on save.

### 7.3 Category (`rental.models.car.Category`)
- Fields: `name`, `slug`, `icon`, `description`.
- Behavior: auto-generates slug; plural verbose name is "Categories".

### 7.4 Car (`rental.models.car.Car`)
- Core fields: `brand`, `category`, `model_name`, `year`, `price_per_day`, `fuel_type`, `transmission`, `seats`, `mileage`.
- Feature flags: `air_conditioning`, `gps`, `bluetooth`.
- Commerce/status: `is_available`, `rating`.
- Media: `main_image`.
- Audit: `created_at`, `updated_at`.
- Properties:
  - `name`: formatted brand + model.
  - `image_url`: resolves media URL or fallback placeholder.

### 7.5 CarImage (`rental.models.car.CarImage`)
- Fields: `car`, `image`.
- Property `image_url` falls back to parent car image URL.

### 7.6 Coupon (`rental.models.booking.Coupon`)
- Fields: `code`, `discount_percentage`, `active`, `valid_from`, `valid_to`.

### 7.7 Booking (`rental.models.booking.Booking`)
- Links: `user`, `car`, optional `coupon_applied`.
- Rental fields: pickup/return dates and locations.
- Financial fields: `rental_days`, `rental_cost`, `tax_amount`, `discount_amount`, `grand_total`.
- Status: `Pending`, `Confirmed`, `Completed`, `Cancelled`.
- Reference: auto-generated `booking_reference` (`DE-XXXXXXXX`).
- Audit: `created_at`, `updated_at`.

### 7.8 Payment (`rental.models.booking.Payment`)
- One-to-one with booking.
- Fields: `amount`, `payment_date`, `payment_method`, `transaction_id`, `status`.
- Methods: `Card`, `PayPal`, `Cash`; statuses: `Pending`, `Completed`, `Failed`.

### 7.9 Wishlist (`rental.models.wishlist.Wishlist`)
- One-to-one with user.
- Many-to-many relation to cars.

### 7.10 Review (`rental.models.interactions.Review`)
- Fields: `user`, `car`, `rating`, `comment`, `created_at`.
- Ordered descending by creation time.

### 7.11 ContactMessage (`rental.models.interactions.ContactMessage`)
- Fields: `name`, `email`, `subject`, `message`, `is_read`, `created_at`.
- Ordered descending by creation time.

### 7.12 Testimonial (`rental.models.interactions.Testimonial`)
- Fields: `user` (nullable), `name`, `designation`, `message`, `rating`, `avatar`, `is_active`, `created_at`.

---

## 8) Application Flows and Business Rules

### 8.1 Authentication and Profile
- Signup enforces password complexity and email uniqueness.
- Login supports username **or** email resolution.
- Forgot/reset password is simulated in-app (no outbound email integration).
- Profile edit supports avatar upload.
- Password change validates current password and keeps session active.

### 8.2 Car Catalog
- Listing endpoint supports filters: search text, brand, category, min/max price, transmission, fuel type, seats.
- Sorting options: popularity (default), newest, price asc/desc.
- Paginated at 6 cars/page.
- Suggestions endpoint returns lightweight JSON for autocomplete.

### 8.3 Review and Rating Update
- Authenticated users can post reviews on car detail page.
- Car rating is recalculated as the average of all persisted reviews.

### 8.4 Wishlist
- Per-user wishlist created lazily (`get_or_create`).
- AJAX toggle endpoint adds/removes car and returns updated count.

### 8.5 Booking and Checkout
- Booking form validates date consistency.
- Checkout preloads search dates/locations when present.
- Price calculation is centralized in `calculate_booking_details` and re-run server-side at booking submit to prevent tampering.
- Tax rate is 15%.
- Coupon must be active and within validity window.
- Successful booking marks car unavailable.

### 8.6 Payment Processing (Mock)
- On booking submit, a payment row is created with generated transaction ID.
- Card/PayPal mark payment `Completed`; Cash remains `Pending`.

### 8.7 Booking Cancellation
- Allowed only for `Pending`/`Confirmed` bookings.
- Cancellation sets booking status to `Cancelled` and returns car to available state.

### 8.8 Contact and Testimonials
- Contact form persists support messages.
- Home page displays active testimonials.

---

## 9) API and Route Surface

### Public Pages
- `GET /` → Home
- `GET /about/` → About
- `GET|POST /contact/` → Contact form

### Authentication and User
- `GET|POST /signup/`
- `GET|POST /login/`
- `GET /logout/`
- `GET|POST /forgot-password/`
- `GET|POST /reset-password/<user_id>/`
- `GET /dashboard/`
- `GET|POST /dashboard/profile/`
- `GET|POST /dashboard/change-password/`

### Cars and Wishlist
- `GET /cars/`
- `GET /cars/suggestions/` (JSON)
- `GET|POST /cars/detail/<pk>/`
- `POST /wishlist/toggle/<car_id>/` (JSON)

### Booking and Payments
- `GET|POST /booking/checkout/<car_id>/`
- `GET /booking/success/<booking_id>/`
- `GET /booking/coupon-check/<car_id>/?code=...` (JSON)
- `GET /dashboard/bookings/`
- `GET /dashboard/bookings/<booking_id>/`
- `POST|GET /dashboard/bookings/<booking_id>/cancel/`

### Custom Admin
- `GET /custom-admin/`
- `GET /custom-admin/<model_name>/`
- `GET|POST /custom-admin/<model_name>/add/`
- `GET|POST /custom-admin/<model_name>/edit/<pk>/`
- `GET|POST /custom-admin/<model_name>/delete/<pk>/`

---

## 10) Forms and Validation Coverage

### Auth Forms (`rental/forms/auth.py`)
- `UserSignupForm`: enforces password policy and confirm-password matching.
- `UserLoginForm`: username/email + remember me.
- `UserProfileForm`: profile fields; email rendered non-editable.
- `ChangePasswordForm`: validates complexity and confirmation.

### Booking Forms (`rental/forms/booking.py`)
- `BookingForm`: date input constraints; prohibits past pickup and invalid return chronology.
- `PaymentMockForm`: conditionally validates card or PayPal details by method.

### Contact/Review Forms (`rental/forms/contact.py`)
- `ContactForm`, `TestimonialForm`, `ReviewForm` for interaction entities.

---

## 11) Admin and Operations

### 11.1 Django Admin
- Route `/admin/` available via built-in Django admin.
- `rental/admin.py` currently contains no explicit model registrations.

### 11.2 Custom Admin Dashboard
File: `rental/views/custom_admin.py`
- Access control: `is_staff` OR `is_staff_admin` OR `is_superuser`.
- KPI metrics: total revenue, total bookings, active bookings, total cars.
- Charts:
  - 6-month revenue trend.
  - booking-status distribution.
- Generic CRUD for mapped models:
  - users, cars, brands, categories, bookings, payments, messages, testimonials, coupons.

---

## 12) Shared Context and UI Data

`rental/context_processors.py` injects:
- `global_categories`, `global_brands` for global navigation/filter UI.
- `wishlist_count` for authenticated users.
- `unread_messages_count` for staff/admin users.

This ensures consistent header/nav counters and category/brand availability across templates.

---

## 13) Data Seeding
`populate_db.py` is available to create demo data, including:
- sample users,
- brands/categories/cars,
- coupons/testimonials/messages.

Use for local demo environments only.

---

## 14) Local Setup and Runbook

### Prerequisites
- Python 3.12+ recommended
- MySQL Server running
- Database `driveease_db` created

### Installation
```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

### Database and Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Optional Seed Data
```bash
python populate_db.py
```

### Run Server
```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

---

## 15) Security and Compliance Notes
Current implementation includes:
- Password strength checks in custom auth forms.
- Server-side re-calculation of booking totals.
- Login and role decorators for protected routes.

Before production deployment, address:
- Move `SECRET_KEY` and DB credentials to environment variables.
- Set `DEBUG=False` and restrict `ALLOWED_HOSTS`.
- Add secure cookie/session/HSTS settings.
- Integrate real password reset email flow.
- Add CSRF/session hardening review and audit logging.

---

## 16) Known Limitations
- Payment is simulated, not gateway-backed.
- Password reset is simulated and exposes reset link in UI.
- Car availability is binary and may require stricter overlap/race handling for high-concurrency production usage.
- Comprehensive automated tests are not yet implemented.

---

## 17) Recommended Enhancements
- Real payment gateway and webhook reconciliation.
- Email/SMS notifications for booking lifecycle events.
- Booking overlap prevention with transactional guarantees.
- REST API layer (DRF) for mobile/third-party clients.
- Expanded test suite (unit, integration, security, and regression).
- Production-ready observability (structured logs, metrics, tracing).

---

## 18) Troubleshooting Quick Reference
- **MySQL connection errors:** verify DB exists and credentials match `settings.py`.
- **Media not loading in dev:** ensure `MEDIA_ROOT` exists and `DEBUG=True` while local serving.
- **Static styling missing:** run `collectstatic` if needed and verify static paths.
- **Auth-related migration issues:** ensure custom user model migration is applied from initial setup.

---

## 19) Appendix: Source Index
Primary implementation files:
- Settings and routing: `driveease/settings.py`, `driveease/urls.py`, `rental/urls.py`
- Domain models: `rental/models/*.py`
- Request handlers: `rental/views/*.py`
- Input validation: `rental/forms/*.py`
- Shared helpers/context: `rental/utilities/helpers.py`, `rental/context_processors.py`
- UX layer: `templates/**`, `static/**`

This document is intended to be the canonical technical reference for contributors and reviewers working on this repository.
