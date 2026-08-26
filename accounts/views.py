from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegisterForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        # no reason for an already-logged-in user to see the register page
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # UserCreationForm.save() already handles password hashing

            # phone isn't part of the User model, so it goes on Profile
            # right after the user is created
            Profile.objects.create(user=user, phone=form.cleaned_data['phone'])

            login(request, user)  # log them straight in rather than making them log in again immediately after
            messages.success(request, f"Welcome to Driftwood Motors, {user.first_name}!")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})