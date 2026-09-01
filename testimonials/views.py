from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Testimonial


def testimonials_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to post a testimonial.")
            return redirect('login')

        message = request.POST.get('message', '').strip()
        rating = request.POST.get('rating', 5)

        if message:
            Testimonial.objects.create(user=request.user, message=message, rating=rating)
            messages.success(request, "Thank you for sharing your experience!")
        else:
            messages.error(request, "Please write a message before submitting.")
        return redirect('testimonials')

    testimonials = Testimonial.objects.filter(is_active=True).select_related('user')
    return render(request, 'testimonials/testimonials.html', {'testimonials': testimonials})