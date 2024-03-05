from django.shortcuts import render, redirect, reverse
from userauths.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from userauths.models import Profile


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are registered")
        return redirect("core:feed")
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        fullname = form.cleaned_data["full_name"]
        phone = form.cleaned_data["phone"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(email=email, password=password)
        login(request, user)
        profile = Profile.objects.get(user=request.user)
        profile.full_name = fullname
        profile.phone = phone
        profile.save()
        messages.success(request, f"Hi {fullname}.your account was created successfully")
        return redirect('core:feed')

    context = {
        "form": form
    }
    return render(request, 'userauths/login_register.html', context)
