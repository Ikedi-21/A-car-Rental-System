from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Car, Brand


def car_list_view(request):
    cars = Car.objects.filter(is_available=True).select_related('brand')

    # --- filtering ---
    # everything comes straight from GET params, no session state involved,
    # so the URL itself represents the exact filter combination applied
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        cars = cars.filter(category__in=selected_categories)

    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        cars = cars.filter(brand_id__in=selected_brands)

    selected_fuel_types = request.GET.getlist('fuel_type')
    if selected_fuel_types:
        cars = cars.filter(fuel_type__in=selected_fuel_types)

    selected_transmission = request.GET.get('transmission')
    if selected_transmission:
        cars = cars.filter(transmission=selected_transmission)

    min_price = request.GET.get('min_price')
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)

    # --- sorting ---
    sort = request.GET.get('sort', 'price_asc')
    sort_map = {
        'price_asc': 'price_per_day',
        'price_desc': '-price_per_day',
        'newest': '-created_at',
    }
    cars = cars.order_by(sort_map.get(sort, 'price_per_day'))

    # --- pagination ---
    paginator = Paginator(cars, 9)  # 9 = clean 3x3 grid on desktop
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)

    context = {
        'cars': cars_page,
        'brands': Brand.objects.all(),
        'category_choices': Car.CATEGORY_CHOICES,
        'fuel_choices': Car.FUEL_CHOICES,
        'selected_categories': selected_categories,
        'selected_brands': selected_brands,
        'selected_fuel_types': selected_fuel_types,
        'selected_transmission': selected_transmission,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        # used by the sort dropdown's hidden form so it can resubmit the
        # existing filters alongside the new sort value
        'current_filters': {
            'category': selected_categories,
            'brand': selected_brands,
            'fuel_type': selected_fuel_types,
        },
    }
    return render(request, 'cars/car_list.html', context)


def car_detail_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # same category, exclude the current car, cap at 3 — matches the
    # "Explore Similar Vehicles" row in the design
    similar_cars = Car.objects.filter(
        category=car.category, is_available=True
    ).exclude(id=car.id).select_related('brand')[:3]

    context = {
        'car': car,
        'similar_cars': similar_cars,
    }
    return render(request, 'cars/car_detail.html', context)