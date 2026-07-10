from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rental.models.car import Car, Category, Brand
from rental.models.interactions import Review
from rental.models.wishlist import Wishlist
from rental.forms.contact import ReviewForm
from django.db.models import Q

def car_list_view(request):
    """
    Renders the Car Catalog page with advanced sidebar filtering, searching,
    sorting, and pagination.
    """
    cars = Car.objects.filter(is_available=True)
    
    # Get parameters
    q = request.GET.get('q', '').strip()
    brand_slug = request.GET.get('brand', '')
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    transmission = request.GET.get('transmission', '')
    fuel_type = request.GET.get('fuel_type', '')
    seats = request.GET.get('seats', '')
    sort_by = request.GET.get('sort_by', 'popularity')
    
    # Apply filters
    if q:
        cars = cars.filter(
            Q(model_name__icontains=q) | 
            Q(brand__name__icontains=q) | 
            Q(category__name__icontains=q)
        )
    if brand_slug:
        cars = cars.filter(brand__slug=brand_slug)
    if category_slug:
        cars = cars.filter(category__slug=category_slug)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if seats:
        cars = cars.filter(seats=seats)
        
    # Apply sorting
    if sort_by == 'newest':
        cars = cars.order_by('-year')
    elif sort_by == 'price_asc':
        cars = cars.order_by('price_per_day')
    elif sort_by == 'price_desc':
        cars = cars.order_by('-price_per_day')
    else: # popularity
        cars = cars.order_by('-rating', '-id')

    # Pagination: 6 cars per page
    paginator = Paginator(cars, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get wishlist items for logged in users to render active heart icons
    wishlist_car_ids = []
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_car_ids = wishlist.cars.values_list('id', flat=True)

    context = {
        'page_obj': page_obj,
        'brands': Brand.objects.all(),
        'categories': Category.objects.all(),
        'wishlist_car_ids': wishlist_car_ids,
        'filters': {
            'q': q,
            'brand': brand_slug,
            'category': category_slug,
            'min_price': min_price,
            'max_price': max_price,
            'transmission': transmission,
            'fuel_type': fuel_type,
            'seats': seats,
            'sort_by': sort_by
        }
    }
    return render(request, 'cars/list.html', context)

def search_suggestions_view(request):
    """
    JSON API endpoint that outputs query suggestions based on partial user input.
    """
    q = request.GET.get('q', '').strip()
    results = []
    if len(q) >= 2:
        cars = Car.objects.filter(
            Q(model_name__icontains=q) | 
            Q(brand__name__icontains=q)
        ).select_related('brand')[:5]
        
        for car in cars:
            results.append({
                'id': car.id,
                'model_name': car.model_name,
                'brand': car.brand.name,
                'price_per_day': float(car.price_per_day),
                'fuel_type': car.fuel_type
            })
            
    return JsonResponse({'results': results})

def car_detail_view(request, pk):
    """
    Displays the details page for a car: specifications, reviews, gallery slider,
    and a checkout reservation widget. Also processes customer review submissions.
    """
    car = get_object_or_404(Car, pk=pk)
    gallery_images = car.images.all()
    reviews = car.reviews.all().select_related('user')
    
    # Check if this car is in user's wishlist
    is_in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        is_in_wishlist = wishlist.cars.filter(id=car.id).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            
            # Recalculate car's average rating
            reviews_list = car.reviews.all()
            total_rating = sum([r.rating for r in reviews_list])
            car.rating = total_rating / len(reviews_list)
            car.save()
            
            messages.success(request, "Thank you! Your review has been published.")
            return redirect('car_detail', pk=car.pk)
        else:
            messages.error(request, "There was an issue saving your review.")
    else:
        review_form = ReviewForm()

    context = {
        'car': car,
        'gallery_images': gallery_images,
        'reviews': reviews,
        'review_form': review_form,
        'is_in_wishlist': is_in_wishlist,
        # Re-check related cars
        'similar_cars': Car.objects.filter(category=car.category, is_available=True).exclude(pk=car.pk)[:3]
    }
    return render(request, 'cars/detail.html', context)

@login_required
def wishlist_toggle_view(request, car_id):
    """
    AJAX endpoint for logged-in users to toggle cars in/out of their wishlist.
    """
    car = get_object_or_404(Car, id=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if wishlist.cars.filter(id=car.id).exists():
        wishlist.cars.remove(car)
        action = 'removed'
    else:
        wishlist.cars.add(car)
        action = 'added'
        
    wishlist_count = wishlist.cars.count()
    return JsonResponse({
        'status': 'success',
        'action': action,
        'wishlist_count': wishlist_count
    })
