from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import RegisterForm, ProfileForm
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



@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
        if form.is_valid():
            form.instance.user = request.user  # make sure save() has access to the User to update
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # without this, Django logs the user out immediately after a
            # password change because the session hash no longer matches
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})