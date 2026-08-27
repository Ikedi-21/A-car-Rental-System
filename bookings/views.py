from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cars.models import Car
from .models import Booking


@login_required
def create_booking_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')
        pickup_location = request.POST.get('pickup_location')

        # total_price is recalculated here server-side rather than trusted
        # from the JS-displayed total on the detail page — a user could
        # tamper with a hidden field, but they can't tamper with this
        from datetime import datetime
        d1 = datetime.strptime(pickup_date, '%Y-%m-%d')
        d2 = datetime.strptime(return_date, '%Y-%m-%d')
        days = (d2 - d1).days

        if days <= 0:
            messages.error(request, "Return date must be after pickup date.")
            return redirect('car_detail', car_id=car.id)

        Booking.objects.create(
            user=request.user,
            car=car,
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=pickup_location,
            total_price=days * car.price_per_day,
        )
        messages.success(request, f"Booking request submitted for {car.brand.name} {car.name}.")
        return redirect('booking_history')

    return redirect('car_detail', car_id=car.id)


@login_required
def booking_history_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related('car', 'car__brand')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})