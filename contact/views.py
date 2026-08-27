from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, SubscribeForm
from .models import ContactDetails


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent — we'll get back to you shortly.")
            return redirect('contact')  # redirect-after-post pattern, stops a page refresh from resubmitting the form
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    # get_or_create means the page never crashes even if no admin has set
    # up contact details yet — it just shows blank fields until they do
    details, _ = ContactDetails.objects.get_or_create(pk=1)

    context = {
        'form': form,
        'details': details,
    }
    return render(request, 'pages/contact.html', context)


def subscribe_view(request):
    """
    Handles the newsletter signup form in the footer. This lives on its
    own endpoint (not folded into contact_view) since the footer form
    appears on every page, not just the contact page — it needs a URL
    that works regardless of which page the POST came from.
    """
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You're subscribed! Watch your inbox for exclusive offers.")
        else:
            # most likely error here is "already subscribed" — surfacing
            # the specific message rather than a generic one
            error_text = form.errors.get('email', ["Something went wrong."])[0]
            messages.error(request, error_text)

    # redirect back to wherever the form was submitted from, falling back
    # to home if that header isn't present for some reason
    return redirect(request.META.get('HTTP_REFERER', 'home'))