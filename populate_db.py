import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'driveease.settings')
django.setup()

from django.contrib.auth import get_user_model
from rental.models.car import Brand, Category, Car
from rental.models.booking import Coupon
from rental.models.interactions import Testimonial, Review, ContactMessage

User = get_user_model()

def populate():
    print("Starting database population script...")

    # 1. Create Users
    print("Creating testing user profiles...")
    
    # Create Staff/Superuser
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@driveease.com',
            password='Admin123!',
            first_name='Marcus',
            last_name='Vance',
            phone='+1 (800) 555-0100',
            bio='DriveEase CEO and chief fleet manager.'
        )
        admin_user.is_staff_admin = True
        admin_user.save()
        print("  Superuser created: username='admin', password='Admin123!'")
    else:
        print("  Superuser 'admin' already exists.")

    # Create Standard Customer
    customer_user = User.objects.filter(username='customer').first()
    if not customer_user:
        customer_user = User.objects.create_user(
            username='customer',
            email='customer@gmail.com',
            password='Customer123!',
            first_name='John',
            last_name='Doe',
            phone='+1 (555) 123-4567',
            bio='Regular business traveler and sports car lover.'
        )
        print("  Customer created: username='customer', password='Customer123!'")
    else:
        print("  Customer 'customer' already exists.")

    # 2. Create Categories
    print("Creating vehicle categories...")
    categories_data = [
        {'name': 'SUV', 'icon': 'fa-truck-monster', 'description': 'Sport Utility Vehicles for off-road and family journeys.'},
        {'name': 'Sedan', 'icon': 'fa-car', 'description': 'Comfortable business and executive sedans.'},
        {'name': 'Luxury', 'icon': 'fa-crown', 'description': 'Elite and premium cars for absolute VIP comfort.'},
        {'name': 'Electric', 'icon': 'fa-charging-station', 'description': 'Eco-friendly, modern electric vehicles with high battery range.'},
        {'name': 'Sports', 'icon': 'fa-gauge-high', 'description': 'Supercars for ultimate track speed and high performance.'},
    ]
    categories = {}
    for c_info in categories_data:
        cat, created = Category.objects.get_or_create(
            name=c_info['name'],
            defaults={'icon': c_info['icon'], 'description': c_info['description']}
        )
        categories[c_info['name']] = cat
        if created:
            print(f"  Category '{c_info['name']}' created.")

    # 3. Create Brands
    print("Creating brands...")
    brands_data = ['Tesla', 'Mercedes', 'BMW', 'Audi', 'Porsche']
    brands = {}
    for b_name in brands_data:
        brand, created = Brand.objects.get_or_create(name=b_name)
        brands[b_name] = brand
        if created:
            print(f"  Brand '{b_name}' created.")

    # 4. Create Cars
    print("Creating premium fleet vehicles...")
    cars_data = [
        {
            'brand': 'Tesla',
            'category': 'Electric',
            'model_name': 'Model S Plaid',
            'year': 2024,
            'price_per_day': 149.00,
            'fuel_type': 'Electric',
            'transmission': 'Automatic',
            'seats': 5,
            'mileage': 600,
            'description': 'The Model S Plaid has the quickest acceleration of any vehicle in production. With 1,020 horsepower, three electric motors, and a carbon-sleeved rotor, it reaches 0-60 mph in 1.99 seconds.',
            'rating': 4.95,
        },
        {
            'brand': 'Tesla',
            'category': 'SUV',
            'model_name': 'Model Y Long Range',
            'year': 2023,
            'price_per_day': 99.00,
            'fuel_type': 'Electric',
            'transmission': 'Automatic',
            'seats': 7,
            'mileage': 533,
            'description': 'Model Y is fully electric, so you never need to visit a gas station again. With 7 seats and maximum cargo volume capacity, it is the perfect family SUV.',
            'rating': 4.80,
        },
        {
            'brand': 'Mercedes',
            'category': 'Luxury',
            'model_name': 'S-Class S580',
            'year': 2024,
            'price_per_day': 220.00,
            'fuel_type': 'Hybrid',
            'transmission': 'Automatic',
            'seats': 5,
            'mileage': 12,
            'description': 'The Mercedes S-Class is the ultimate expression of luxury and prestige. Featuring soft leather seats, ambient lighting, dual executive rear climate zones, and unmatched cabin insulation.',
            'rating': 5.00,
        },
        {
            'brand': 'Mercedes',
            'category': 'SUV',
            'model_name': 'GLE 450 AMG',
            'year': 2023,
            'price_per_day': 130.00,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'seats': 5,
            'mileage': 10,
            'description': 'GLE Coupe design blends high-riding SUV versatility with sleek coupe aerodynamics. Equipped with an AMG-enhanced inline-6 engine and active 4MATIC traction controls.',
            'rating': 4.85,
        },
        {
            'brand': 'BMW',
            'category': 'Sports',
            'model_name': 'M4 Competition',
            'year': 2024,
            'price_per_day': 180.00,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'seats': 4,
            'mileage': 9,
            'description': 'The BMW M4 Competition Coupe models combine premium design, high-performance mechanical parts, and intelligent digital drive assisting modules for the ultimate track experience.',
            'rating': 4.90,
        },
        {
            'brand': 'BMW',
            'category': 'Sedan',
            'model_name': '5 Series 530i',
            'year': 2023,
            'price_per_day': 89.00,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'seats': 5,
            'mileage': 14,
            'description': 'Elegant, business-centric executive sedan. Offers dynamic handling, modern virtual cockpit, active driving assistance lane control, and comfortable leather seating.',
            'rating': 4.75,
        },
        {
            'brand': 'Audi',
            'category': 'Sports',
            'model_name': 'R8 V10 Performance',
            'year': 2023,
            'price_per_day': 299.00,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'seats': 2,
            'mileage': 6,
            'description': 'Mid-engine supercar featuring a naturally aspirated 5.2-liter V10 engine. The Audi R8 provides raw racing power, signature Quattro all-wheel drive stability, and distinct carbon fiber aesthetics.',
            'rating': 4.98,
        },
        {
            'brand': 'Porsche',
            'category': 'Sports',
            'model_name': '911 Carrera S',
            'year': 2024,
            'price_per_day': 240.00,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'seats': 4,
            'mileage': 8,
            'description': 'The iconic sports car. Unmatched rear-engine balance, active steering, and PDK dual-clutch transmission make the Porsche 911 the enthusiast choice for coastal cruises.',
            'rating': 5.00,
        }
    ]

    for c_info in cars_data:
        # Avoid duplicates
        brand_obj = brands[c_info['brand']]
        cat_obj = categories[c_info['category']]
        
        car_obj = Car.objects.filter(brand=brand_obj, model_name=c_info['model_name']).first()
        if not car_obj:
            # We can download a dummy image or leave placeholder
            # For testing, we just use a generic file upload value
            # Let's assign an empty image field or standard path
            car_obj = Car.objects.create(
                brand=brand_obj,
                category=cat_obj,
                model_name=c_info['model_name'],
                year=c_info['year'],
                price_per_day=c_info['price_per_day'],
                fuel_type=c_info['fuel_type'],
                transmission=c_info['transmission'],
                seats=c_info['seats'],
                mileage=c_info['mileage'],
                description=c_info['description'],
                rating=c_info['rating'],
                main_image='cars/default_car.jpg' # Seed files
            )
            print(f"  Car '{brand_obj.name} {c_info['model_name']}' created.")
        else:
            print(f"  Car '{brand_obj.name} {c_info['model_name']}' already exists.")

    # 5. Create Coupons
    print("Creating coupons...")
    now = timezone.now()
    future = now + timedelta(days=365)
    
    coupons_data = [
        {'code': 'DRIVEEASE20', 'discount_percentage': 20},
        {'code': 'WELCOME10', 'discount_percentage': 10},
    ]
    for cp in coupons_data:
        coupon, created = Coupon.objects.get_or_create(
            code=cp['code'],
            defaults={
                'discount_percentage': cp['discount_percentage'],
                'active': True,
                'valid_from': now,
                'valid_to': future
            }
        )
        if created:
            print(f"  Coupon '{cp['code']}' created.")

    # 6. Create Testimonials
    print("Creating testimonials...")
    testimonials_data = [
        {
            'name': 'Sarah Jenkins',
            'designation': 'Marketing Director',
            'message': 'Renting the S-Class S580 for our corporate partners was an absolute success. The service represents pure luxury.',
            'rating': 5
        },
        {
            'name': 'Devon Miller',
            'designation': 'Freelance Designer',
            'message': 'The Tesla Model S Plaid is completely insane! DriveEase checkout process took under 3 minutes, highly recommended.',
            'rating': 5
        }
    ]
    for t_info in testimonials_data:
        t, created = Testimonial.objects.get_or_create(
            name=t_info['name'],
            message=t_info['message'],
            defaults={'designation': t_info['designation'], 'rating': t_info['rating'], 'is_active': True}
        )
        if created:
            print(f"  Testimonial from '{t_info['name']}' created.")

    # 7. Create mock Support Messages
    print("Creating mock Contact Messages...")
    msgs_data = [
        {
            'name': 'Alice Smith',
            'email': 'alice@gmail.com',
            'subject': 'Corporate Fleet Discount Queries',
            'message': 'Hello, we are looking to lease 4 luxury vehicles for an executive retreat next week. Do you offer corporate discount codes?'
        }
    ]
    for m in msgs_data:
        msg, created = ContactMessage.objects.get_or_create(
            name=m['name'],
            subject=m['subject'],
            defaults={'email': m['email'], 'message': m['message'], 'is_read': False}
        )
        if created:
            print(f"  Contact Message from '{m['name']}' created.")

    print("\nDatabase pre-population completed successfully!")

if __name__ == '__main__':
    populate()
