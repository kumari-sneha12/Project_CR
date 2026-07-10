from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.utils import timezone
from django.forms import modelform_factory
from django import forms
from decimal import Decimal
import json

# Import all models dynamically to reference in generic CRUD views
from rental.models.auth import User
from rental.models.car import Car, Brand, Category, CarImage
from rental.models.booking import Booking, Payment, Coupon
from rental.models.interactions import Review, ContactMessage, Testimonial

# Helper list of models allowed for admin control
MODEL_MAP = {
    'users': User,
    'cars': Car,
    'brands': Brand,
    'categories': Category,
    'bookings': Booking,
    'payments': Payment,
    'messages': ContactMessage,
    'testimonials': Testimonial,
    'coupons': Coupon,
}

def is_staff_check(user):
    """
    Verifies if user has staff privileges.
    """
    return user.is_authenticated and (user.is_staff or getattr(user, 'is_staff_admin', False) or user.is_superuser)

@user_passes_test(is_staff_check, login_url='login')
def dashboard_view(request):
    """
    Renders custom admin dashboard metrics and Chart.js feeds.
    """
    total_revenue = Payment.objects.filter(status='Completed').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status__in=['Pending', 'Confirmed']).count()
    total_cars = Car.objects.count()

    # Past 6 Months Revenue Trend
    months = []
    amounts = []
    now = timezone.now()
    for i in range(5, -1, -1):
        # Rough calculation of month ranges
        start_month = (now.month - i - 1) % 12 + 1
        year_offset = (now.month - i - 1) // 12
        year = now.year + year_offset
        
        month_payments = Payment.objects.filter(
            status='Completed',
            payment_date__year=year,
            payment_date__month=start_month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Format month names
        date_dummy = timezone.datetime(year, start_month, 1)
        months.append(date_dummy.strftime('%b %Y'))
        amounts.append(float(month_payments))

    # Booking Status distribution counts
    statuses = ['Pending', 'Confirmed', 'Completed', 'Cancelled']
    counts = []
    for s in statuses:
        counts.append(Booking.objects.filter(status=s).count())

    recent_bookings = Booking.objects.order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.filter(is_read=False).order_by('-created_at')[:5]

    context = {
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'total_cars': total_cars,
        'months_json': json.dumps(months),
        'amounts_json': json.dumps(amounts),
        'statuses_json': json.dumps(statuses),
        'counts_json': json.dumps(counts),
        'recent_bookings': recent_bookings,
        'recent_messages': recent_messages
    }
    return render(request, 'custom_admin/dashboard.html', context)

@user_passes_test(is_staff_check, login_url='login')
def manage_list_view(request, model_name):
    """
    Generic model list rendering with search query processing, filters, and pagination.
    """
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        messages.error(request, f"Model '{model_name}' is not registered in admin mapping.")
        return redirect('custom_admin_dashboard')
        
    records = model.objects.all()

    # Simple dynamic searching based on common attributes
    q = request.GET.get('q', '').strip()
    if q:
        if hasattr(model, 'username'):
            records = records.filter(username__icontains=q)
        elif hasattr(model, 'model_name'):
            records = records.filter(model_name__icontains=q)
        elif hasattr(model, 'name'):
            records = records.filter(name__icontains=q)
        elif hasattr(model, 'booking_reference'):
            records = records.filter(booking_reference__icontains=q)
        elif hasattr(model, 'transaction_id'):
            records = records.filter(transaction_id__icontains=q)
        elif hasattr(model, 'subject'):
            records = records.filter(subject__icontains=q)
            
    # Mark messages as read if accessed via admin message detail page optionally
    if model_name.lower() == 'messages' and 'read' in request.GET:
        msg_id = request.GET.get('read')
        ContactMessage.objects.filter(id=msg_id).update(is_read=True)

    # Paginate admin lists: 10 records per page
    paginator = Paginator(records.order_by('-id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'model_name': model_name.capitalize(),
        'model_slug': model_name.lower(),
        'search_query': q,
    }
    return render(request, 'custom_admin/manage_list.html', context)

@user_passes_test(is_staff_check, login_url='login')
def manage_create_view(request, model_name):
    """
    Generates dynamic Creation Forms based on Model specs and saves new instances.
    """
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        messages.error(request, "Invalid admin module.")
        return redirect('custom_admin_dashboard')

    # Exclude non-editable auto fields
    FormClass = modelform_factory(model, exclude=['created_at', 'updated_at', 'last_login', 'date_joined', 'groups', 'user_permissions', 'booking_reference', 'transaction_id'])
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            messages.success(request, f"New record in '{model_name.capitalize()}' added successfully.")
            return redirect('custom_admin_list', model_name=model_name)
    else:
        form = FormClass()

    # Style form widgets with Bootstrap
    for field in form.fields.values():
        if isinstance(field.widget, (forms.CheckboxInput, forms.NullBooleanSelect)):
            field.widget.attrs.update({'class': 'form-check-input'})
        else:
            field.widget.attrs.update({'class': 'form-control'})

    context = {
        'form': form,
        'model_name': model_name.capitalize(),
        'model_slug': model_name.lower(),
        'action': 'Create'
    }
    return render(request, 'custom_admin/manage_form.html', context)

@user_passes_test(is_staff_check, login_url='login')
def manage_update_view(request, model_name, pk):
    """
    Generates dynamic Update Forms based on Model specs and updates matching records.
    """
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        messages.error(request, "Invalid admin module.")
        return redirect('custom_admin_dashboard')

    instance = get_object_or_404(model, pk=pk)
    FormClass = modelform_factory(model, exclude=['created_at', 'updated_at', 'last_login', 'date_joined', 'groups', 'user_permissions', 'booking_reference', 'transaction_id'])
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Record in '{model_name.capitalize()}' updated successfully.")
            return redirect('custom_admin_list', model_name=model_name)
    else:
        form = FormClass(instance=instance)

    # Style form widgets with Bootstrap
    for field in form.fields.values():
        if isinstance(field.widget, (forms.CheckboxInput, forms.NullBooleanSelect)):
            field.widget.attrs.update({'class': 'form-check-input'})
        else:
            field.widget.attrs.update({'class': 'form-control'})

    context = {
        'form': form,
        'model_name': model_name.capitalize(),
        'model_slug': model_name.lower(),
        'action': 'Update'
    }
    return render(request, 'custom_admin/manage_form.html', context)

@user_passes_test(is_staff_check, login_url='login')
def manage_delete_view(request, model_name, pk):
    """
    Deletes the selected model record.
    """
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        messages.error(request, "Invalid admin module.")
        return redirect('custom_admin_dashboard')

    instance = get_object_or_404(model, pk=pk)
    instance.delete()
    messages.success(request, f"Record from '{model_name.capitalize()}' deleted successfully.")
    return redirect('custom_admin_list', model_name=model_name)
