from django.urls import path
from rental.views import home, auth, cars, booking, custom_admin

urlpatterns = [
    # General / Static pages
    path('', home.index, name='home'),
    path('about/', home.about, name='about'),
    path('contact/', home.contact, name='contact'),

    # Authentication & Dashboard
    path('signup/', auth.signup_view, name='signup'),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('forgot-password/', auth.forgot_password_view, name='forgot_password'),
    path('reset-password/<int:user_id>/', auth.reset_password_view, name='reset_password'),
    path('dashboard/', auth.dashboard_view, name='dashboard'),
    path('dashboard/profile/', auth.edit_profile_view, name='edit_profile'),
    path('dashboard/change-password/', auth.change_password_view, name='change_password'),

    # Cars Catalog & Interaction
    path('cars/', cars.car_list_view, name='car_list'),
    path('cars/suggestions/', cars.search_suggestions_view, name='search_suggestions'),
    path('cars/detail/<int:pk>/', cars.car_detail_view, name='car_detail'),
    path('wishlist/toggle/<int:car_id>/', cars.wishlist_toggle_view, name='wishlist_toggle'),

    # Booking & Checkouts
    path('booking/checkout/<int:car_id>/', booking.checkout_view, name='checkout'),
    path('booking/success/<int:booking_id>/', booking.booking_success_view, name='booking_success'),
    path('booking/coupon-check/<int:car_id>/', booking.coupon_check_view, name='coupon_check'),
    path('dashboard/bookings/', booking.my_bookings_view, name='my_bookings'),
    path('dashboard/bookings/<int:booking_id>/', booking.booking_detail_view, name='booking_detail'),
    path('dashboard/bookings/<int:booking_id>/cancel/', booking.cancel_booking_view, name='cancel_booking'),

    # Custom Admin Dashboard
    path('custom-admin/', custom_admin.dashboard_view, name='custom_admin_dashboard'),
    path('custom-admin/<str:model_name>/', custom_admin.manage_list_view, name='custom_admin_list'),
    path('custom-admin/<str:model_name>/add/', custom_admin.manage_create_view, name='custom_admin_create'),
    path('custom-admin/<str:model_name>/edit/<int:pk>/', custom_admin.manage_update_view, name='custom_admin_update'),
    path('custom-admin/<str:model_name>/delete/<int:pk>/', custom_admin.manage_delete_view, name='custom_admin_delete'),
]
