from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from cars.models import Brand, Car
from bookings.models import Booking
from testimonials.models import Testimonial
from contact.models import ContactQuery, Subscriber, ContactDetails
from pages.models import SiteContent


def is_admin(user):
    # is_staff covers Django superusers/staff created via createsuperuser;
    # this is the gate for the entire dashboard app
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    context = {
        'user_count': User.objects.count(),
        'booking_count': Booking.objects.count(),
        'subscriber_count': Subscriber.objects.count(),
        'query_count': ContactQuery.objects.filter(status='new').count(),
        'recent_bookings': Booking.objects.select_related('user', 'car')[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)


# --- Brands ---
@login_required
@user_passes_test(is_admin)
def brand_list_view(request):
    brands = Brand.objects.all()
    return render(request, 'dashboard/brand_list.html', {'brands': brands})


@login_required
@user_passes_test(is_admin)
def brand_form_view(request, brand_id=None):
    brand = get_object_or_404(Brand, id=brand_id) if brand_id else None

    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')

        if brand:
            brand.name = name
            if logo:
                brand.logo = logo
            brand.save()
            messages.success(request, "Brand updated successfully.")
        else:
            Brand.objects.create(name=name, logo=logo)
            messages.success(request, "Brand created successfully.")
        return redirect('admin_brand_list')

    return render(request, 'dashboard/brand_form.html', {'brand': brand})


@login_required
@user_passes_test(is_admin)
def brand_delete_view(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    brand.delete()
    messages.success(request, "Brand deleted.")
    return redirect('admin_brand_list')


# --- Cars ---
@login_required
@user_passes_test(is_admin)
def car_list_admin_view(request):
    cars = Car.objects.select_related('brand').all()
    return render(request, 'dashboard/car_list_admin.html', {'cars': cars})


@login_required
@user_passes_test(is_admin)
def car_form_view(request, car_id=None):
    car = get_object_or_404(Car, id=car_id) if car_id else None
    brands = Brand.objects.all()

    if request.method == 'POST':
        data = {
            'brand_id': request.POST.get('brand'),
            'name': request.POST.get('name'),
            'category': request.POST.get('category'),
            'price_per_day': request.POST.get('price_per_day'),
            'transmission': request.POST.get('transmission'),
            'fuel_type': request.POST.get('fuel_type'),
            'seats': request.POST.get('seats'),
            'description': request.POST.get('description'),
            'is_available': request.POST.get('is_available') == 'on',
            'is_featured': request.POST.get('is_featured') == 'on',
        }
        image = request.FILES.get('image')

        if car:
            for field, value in data.items():
                setattr(car, field, value)
            if image:
                car.image = image
            car.save()
            messages.success(request, "Vehicle updated successfully.")
        else:
            new_car = Car.objects.create(**data)
            if image:
                new_car.image = image
                new_car.save()
            messages.success(request, "Vehicle added successfully.")
        return redirect('admin_car_list')

    return render(request, 'dashboard/car_form.html', {
        'car': car,
        'brands': brands,
        'category_choices': Car.CATEGORY_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'fuel_choices': Car.FUEL_CHOICES,
    })


@login_required
@user_passes_test(is_admin)
def car_delete_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    messages.success(request, "Vehicle deleted.")
    return redirect('admin_car_list')


# --- Bookings ---
@login_required
@user_passes_test(is_admin)
def booking_list_admin_view(request):
    bookings = Booking.objects.select_related('user', 'car', 'car__brand').order_by('-created_at')
    return render(request, 'dashboard/booking_list_admin.html', {'bookings': bookings})


@login_required
@user_passes_test(is_admin)
def booking_update_status_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    new_status = request.POST.get('status')
    if new_status in dict(Booking.STATUS_CHOICES):
        booking.status = new_status
        booking.save()
        messages.success(request, f"Booking marked as {booking.get_status_display()}.")
    return redirect('admin_booking_list')


# --- Testimonials ---
@login_required
@user_passes_test(is_admin)
def testimonial_list_admin_view(request):
    testimonials = Testimonial.objects.select_related('user').order_by('-created_at')
    return render(request, 'dashboard/testimonial_list_admin.html', {'testimonials': testimonials})


@login_required
@user_passes_test(is_admin)
def testimonial_toggle_view(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    testimonial.is_active = not testimonial.is_active
    testimonial.save()
    return redirect('admin_testimonial_list')


# --- Contact Queries ---
@login_required
@user_passes_test(is_admin)
def query_list_admin_view(request):
    queries = ContactQuery.objects.order_by('-created_at')
    return render(request, 'dashboard/query_list_admin.html', {'queries': queries})


@login_required
@user_passes_test(is_admin)
def query_resolve_view(request, query_id):
    query = get_object_or_404(ContactQuery, id=query_id)
    query.status = 'resolved'
    query.save()
    return redirect('admin_query_list')


# --- Users ---
@login_required
@user_passes_test(is_admin)
def user_list_admin_view(request):
    users = User.objects.select_related('profile').order_by('-date_joined')
    return render(request, 'dashboard/user_list_admin.html', {'users': users})


# --- Subscribers ---
@login_required
@user_passes_test(is_admin)
def subscriber_list_admin_view(request):
    subscribers = Subscriber.objects.order_by('-subscribed_at')
    return render(request, 'dashboard/subscriber_list_admin.html', {'subscribers': subscribers})


@login_required
@user_passes_test(is_admin)
def subscriber_delete_view(request, subscriber_id):
    Subscriber.objects.filter(id=subscriber_id).delete()
    messages.success(request, "Subscriber removed.")
    return redirect('admin_subscriber_list')


# --- Site Content ---
@login_required
@user_passes_test(is_admin)
def site_content_view(request):
    contents = SiteContent.objects.all()

    if request.method == 'POST':
        page_key = request.POST.get('page_key')
        title = request.POST.get('title')
        content = request.POST.get('content')
        SiteContent.objects.update_or_create(
            page_key=page_key,
            defaults={'title': title, 'content': content}
        )
        messages.success(request, "Page content updated.")
        return redirect('admin_site_content')

    return render(request, 'dashboard/site_content_form.html', {'contents': contents})


# --- Contact Details ---
@login_required
@user_passes_test(is_admin)
def contact_details_view(request):
    details, _ = ContactDetails.objects.get_or_create(pk=1)

    if request.method == 'POST':
        details.address = request.POST.get('address')
        details.phone = request.POST.get('phone')
        details.email = request.POST.get('email')
        details.map_embed = request.POST.get('map_embed')
        details.save()
        messages.success(request, "Contact details updated.")
        return redirect('admin_contact_details')

    return render(request, 'dashboard/contact_details_form.html', {'details': details})


# --- Admin password ---
@login_required
@user_passes_test(is_admin)
def admin_change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('admin_dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'dashboard/admin_change_password.html', {'form': form})