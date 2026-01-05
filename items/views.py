from django.http import HttpResponse
# Simple view to test CSP headers
def test_csp(request):
    response = HttpResponse("CSP header test page.")
    response["X-Test-Header"] = "deployed"
    return response
import math
from django.shortcuts import render, redirect, get_object_or_404
from .models import RecoveredItem

def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formula to calculate distance between two GPS points."""
    R = 6371.0  # Earth radius in KM
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def item_list(request):
    items = RecoveredItem.objects.all().order_by('-created_at')
    
    # Search and Category Filtering
    q = request.GET.get('q')
    cat = request.GET.get('category')
    
    if q:
        items = items.filter(name__icontains=q) | items.filter(finder_name__icontains=q)
    if cat:
        items = items.filter(category=cat)
    
    # User-to-Item Distance Calculation
    u_lat = request.GET.get('lat')
    u_lng = request.GET.get('lng')
    if u_lat and u_lng:
        try:
            lat, lng = float(u_lat), float(u_lng)
            for item in items:
                item.distance = calculate_distance(lat, lng, item.latitude, item.longitude)
        except (ValueError, TypeError):
            pass
            
    return render(request, 'items/item_list.html', {
        'items': items, 
        'categories': RecoveredItem.CATEGORIES
    })

def upload_item(request):
    if request.method == 'POST':
        # Capture all fields including new finder details
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        RecoveredItem.objects.create(
            name=request.POST.get('name'),
            finder_name=request.POST.get('finder_name'),
            finder_contact=request.POST.get('finder_contact'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            image=request.FILES.get('image'),
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None
        )
        return redirect('item_list')
    return render(request, 'items/upload.html', {'categories': RecoveredItem.CATEGORIES})

def delete_item(request, item_id):
    item = get_object_or_404(RecoveredItem, id=item_id)
    item.delete()
    return redirect('item_list')

def item_detail(request, item_id):
    item = get_object_or_404(RecoveredItem, id=item_id)
    return render(request, 'items/item_detail.html', {
        'item': item, 
        'categories': RecoveredItem.CATEGORIES
    })