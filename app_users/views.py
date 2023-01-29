from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app_users.forms import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


def index(request):
    return render(request, "app_users/index.html")


def register(request):

    registered = False

    if request.method == "POST":
        user_form = userForm(data=request.POST)
        profile_form = UserProfileInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = userForm()
        profile_form = UserProfileInfoForm()

    return render(
        request,
        "app_users/registration.html",
        {
            "registered": registered,
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Account is deactivated")
        else:
            return HttpResponse("Please use correct id and password")

    else:
        return render(request, "app_users/login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def user_profile_view(request):
    user = request.user
    profile = user_profile.objects.get(user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "app_users/profile.html", context)


@login_required
def user_profile_update(request): #function based view
    user = request.user
    profile = user_profile.objects.get(user=user)
    form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            return redirect('user_profile_update')

    context = {
        "user": user,
        "profile": profile,
        "form": form,
    }
    return render(request, "app_users/update-profile.html", context)
