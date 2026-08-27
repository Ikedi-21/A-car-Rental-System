from django.shortcuts import render
from cars.models import Car
from testimonials.models import Testimonial


def home_view(request):
    context = {
        'featured_cars': Car.objects.filter(is_featured=True, is_available=True).select_related('brand')[:4],
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('-created_at')[:2],
    }
    return render(request, 'pages/home.html', context)

def about_view(request):
    return render(request, 'pages/about.html')