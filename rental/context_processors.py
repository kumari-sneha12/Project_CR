from rental.models.car import Category, Brand
from rental.models.wishlist import Wishlist
from rental.models.interactions import ContactMessage

def global_context(request):
    """
    Exposes common variables globally to all Django templates.
    """
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_count = wishlist_item.cars.count()
        
    unread_messages_count = 0
    if request.user.is_authenticated and (request.user.is_staff or getattr(request.user, 'is_staff_admin', False)):
        unread_messages_count = ContactMessage.objects.filter(is_read=False).count()
        
    return {
        'global_categories': categories,
        'global_brands': brands,
        'wishlist_count': wishlist_count,
        'unread_messages_count': unread_messages_count,
    }
