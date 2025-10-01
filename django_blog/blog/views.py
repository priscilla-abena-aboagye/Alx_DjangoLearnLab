from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView

def home(request):
    return render(request, "blog/base.html")

def posts(request):
    return render(request, "blog/posts.html") 

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "blog/login.html"

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        pform = ProfileForm(instance=profile)
    return render(request, "blog/profile.html", {"pform": pform})
