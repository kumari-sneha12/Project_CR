from datetime import datetime, date
from decimal import Decimal
from django.utils import timezone
from rental.models.booking import Coupon

def calculate_booking_details(car, pickup_date, return_date, coupon_code=None):
    """
    Calculates rental days, rental cost, taxes, discount, and grand total.
    Supports inputting either Date objects or string dates formatted as 'YYYY-MM-DD'.
    """
    if isinstance(pickup_date, str):
        try:
            pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()
        except ValueError:
            pickup_date = date.today()

    if isinstance(return_date, str):
        try:
            return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
        except ValueError:
            return_date = date.today()

    if pickup_date >= return_date:
        rental_days = 1
    else:
        rental_days = (return_date - pickup_date).days

    rental_cost = Decimal(str(car.price_per_day)) * rental_days
    tax_rate = Decimal('0.15')  # 15% standard tax
    tax_amount = rental_cost * tax_rate

    discount_amount = Decimal('0.00')
    coupon_applied = None

    if coupon_code:
        try:
            coupon = Coupon.objects.get(
                code__iexact=coupon_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            discount_percentage = Decimal(str(coupon.discount_percentage))
            # Calculate discount on rental cost
            discount_amount = rental_cost * (discount_percentage / Decimal('100.0'))
            coupon_applied = coupon
        except Coupon.DoesNotExist:
            pass

    grand_total = (rental_cost + tax_amount) - discount_amount

    # Formatting values
    rental_cost = rental_cost.quantize(Decimal('0.01'))
    tax_amount = tax_amount.quantize(Decimal('0.01'))
    discount_amount = discount_amount.quantize(Decimal('0.01'))
    grand_total = grand_total.quantize(Decimal('0.01'))

    return {
        'rental_days': rental_days,
        'rental_cost': rental_cost,
        'tax_amount': tax_amount,
        'discount_amount': discount_amount,
        'coupon_applied': coupon_applied,
        'grand_total': grand_total
    }
