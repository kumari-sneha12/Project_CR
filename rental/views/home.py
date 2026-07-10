from django.shortcuts import render, redirect
from django.contrib import messages
from rental.models.car import Car, Category, Brand
from rental.models.interactions import Testimonial, ContactMessage
from rental.forms.contact import ContactForm

def index(request):
    """
    Renders the DriveEase Home page displaying featured cars, categories,
    why choose us, statistics, FAQ, and testimonials.
    """
    featured_cars = Car.objects.filter(is_available=True).order_by('-rating')[:6]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:5]
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    context = {
        'featured_cars': featured_cars,
        'testimonials': testimonials,
        'categories': categories,
        'brands': brands,
        'hero_bg_url': '/static/images/hero_car.jpg' # Can be seeded or uploaded
    }
    return render(request, 'index.html', context)

def about(request):
    """
    Renders the corporate About Us timeline, stats, mission, and team cards.
    """
    team_members = [
        {
            'name': 'Marcus Vance',
            'role': 'CEO & Founder',
            'image_url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=400'
        },
        {
            'name': 'Seraphina Gold',
            'role': 'Head of Design',
            'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=400'
        },
        {
            'name': 'Harrison Ford',
            'role': 'Chief Operations Officer',
            'image_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=400'
        }
    ]
    context = {
        'team_members': team_members
    }
    return render(request, 'about.html', context)

def contact(request):
    """
    Renders the Contact Us form, coordinates, and submits messages to the database.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been received! Our support agents will contact you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Failed to submit message. Please correct the fields below.")
    else:
        form = ContactForm()
        
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)
