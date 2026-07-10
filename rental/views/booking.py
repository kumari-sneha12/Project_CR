from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from rental.models.car import Car
from rental.models.booking import Booking, Payment, Coupon
from rental.forms.booking import BookingForm, PaymentMockForm
from rental.utilities.helpers import calculate_booking_details
import uuid

@login_required
def checkout_view(request, car_id):
    """
    Renders checkout page. Computes booking costs, applies coupon discounts,
    processes payments (mocked), and creates database bookings.
    """
    car = get_object_or_404(Car, id=car_id, is_available=True)
    
    # Pre-populate dates/locations from home search form if available
    initial_data = {
        'pickup_date': request.GET.get('pickup_date', ''),
        'return_date': request.GET.get('return_date', ''),
        'pickup_location': request.GET.get('pickup_location', ''),
        'return_location': request.GET.get('return_location', '')
    }

    booking_form = BookingForm(request.POST or None, initial=initial_data)
    payment_form = PaymentMockForm(request.POST or None)
    coupon_code = request.POST.get('coupon_code', '').strip()

    # Calculate initial estimation (with or without coupon)
    pickup_date_str = request.POST.get('pickup_date') or initial_data['pickup_date'] or timezone.now().date().strftime('%Y-%m-%d')
    return_date_str = request.POST.get('return_date') or initial_data['return_date'] or (timezone.now() + timezone.timedelta(days=1)).date().strftime('%Y-%m-%d')
    
    calc = calculate_booking_details(car, pickup_date_str, return_date_str, coupon_code)

    if request.method == 'POST':
        # Apply coupon code if request has 'apply_coupon' button
        if 'apply_coupon_btn' in request.POST:
            if calc['coupon_applied']:
                messages.success(request, f"Coupon '{coupon_code}' applied successfully! {calc['coupon_applied'].discount_percentage}% off.")
            else:
                messages.error(request, "Invalid, expired, or deactivated coupon code.")
            # Do not save, just return updated calculations
        
        # Process checkout if user clicked 'submit_booking'
        elif 'submit_booking_btn' in request.POST:
            if booking_form.is_valid() and payment_form.is_valid():
                # Re-calculate to prevent price manipulation in frontend
                pickup = booking_form.cleaned_data['pickup_date']
                return_d = booking_form.cleaned_data['return_date']
                
                final_calc = calculate_booking_details(car, pickup, return_d, coupon_code)
                
                # Create Booking object
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.car = car
                booking.rental_days = final_calc['rental_days']
                booking.rental_cost = final_calc['rental_cost']
                booking.tax_amount = final_calc['tax_amount']
                booking.discount_amount = final_calc['discount_amount']
                booking.coupon_applied = final_calc['coupon_applied']
                booking.grand_total = final_calc['grand_total']
                booking.status = 'Confirmed' # Set Confirmed once payment goes through
                booking.save()
                
                # Process Payment details
                payment_method = payment_form.cleaned_data['payment_method']
                transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
                
                payment = Payment.objects.create(
                    booking=booking,
                    amount=booking.grand_total,
                    payment_method=payment_method,
                    transaction_id=transaction_id,
                    status='Completed' if payment_method in ['Card', 'PayPal'] else 'Pending'
                )
                
                # Set car as unavailable for the moment
                car.is_available = False
                car.save()
                
                messages.success(request, "Your booking has been confirmed! Receipt generated.")
                return redirect('booking_success', booking_id=booking.id)
            else:
                # Add validation errors to message store
                for field, errors in booking_form.errors.items():
                    for error in errors:
                        messages.error(request, f"Booking Form ({field}): {error}")
                for field, errors in payment_form.errors.items():
                    for error in errors:
                        messages.error(request, f"Payment Form ({field}): {error}")

    context = {
        'car': car,
        'booking_form': booking_form,
        'payment_form': payment_form,
        'calc': calc,
        'coupon_code': coupon_code,
    }
    return render(request, 'booking/checkout.html', context)

@login_required
def booking_success_view(request, booking_id):
    """
    Renders the booking confirmation and invoice receipt page.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/success.html', {'booking': booking})

@login_required
def my_bookings_view(request):
    """
    Renders user's complete booking list on dashboard.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail_view(request, booking_id):
    """
    Renders a specific invoice details page with custom printable CSS grids.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'dashboard/booking_details.html', {'booking': booking})

@login_required
def cancel_booking_view(request, booking_id):
    """
    Sets booking status to Cancelled and releases the car back to the fleet.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['Pending', 'Confirmed']:
        booking.status = 'Cancelled'
        booking.save()
        
        # Release the car
        car = booking.car
        car.is_available = True
        car.save()
        
        messages.success(request, f"Booking '{booking.booking_reference}' has been successfully cancelled.")
    else:
        messages.error(request, "This booking cannot be cancelled at this stage.")
        
    return redirect('booking_detail', booking_id=booking.id)

def coupon_check_view(request, car_id):
    """
    AJAX endpoint checking coupon codes. Returns discount rate on the fly.
    """
    car = get_object_or_404(Car, id=car_id)
    coupon_code = request.GET.get('code', '').strip()
    
    try:
        coupon = Coupon.objects.get(
            code__iexact=coupon_code,
            active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        )
        return JsonResponse({
            'status': 'success',
            'valid': True,
            'discount_percentage': coupon.discount_percentage
        })
    except Coupon.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'valid': False,
            'discount_percentage': 0
        })
