from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import UserRegisterForm


User = get_user_model()


# Register view
def register_user(request):

    """Registers a user if user is not registered or logged in"""

    # Checking if user is already logged in or not
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False})
    if request.user.is_authenticated:
        return redirect('redirect_origin')

    # If request is post and user is not registered or logged in
    if request.method == 'POST' and not request.user.is_authenticated:

        # Verify the request data and register the user
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            user = authenticate(request, email=form.cleaned_data['email'], password=request.POST['password1'])
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True, 'form_errors': form.errors})

    return render(request, 'register.html')


# Login view
def login_user(request):

    """Logs in a user if user is registered and logged out"""

    # If user is logged in redirect him or return a bad request
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False}, status=403)
    if request.user.is_authenticated:
        return redirect('home')

    # If user is not logged in then initiate login and redirect the user to base location where he came from
    if request.method == 'POST' and not request.user.is_authenticated:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': '/'})
        else:
            return JsonResponse({'error': True})
    return render(request, 'login.html')


# Logout view
@login_required
def logout_user(request):

    """Logs out a user and redirects to login page"""
    if not request.user.is_authenticated:
        return redirect('login')

    logout(request)
    return redirect('login')
