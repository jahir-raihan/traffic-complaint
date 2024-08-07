# Imports

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from complain.models import Complain
from .forms import UserRegisterForm
from django.views import View
from django.db.models import Q

# End Imports


User = get_user_model()


# Register view
def register_user(request):

    """Registers a user if user is not registered or logged in"""

    # Checking if user is already logged in or not
    if request.user.is_authenticated and request.method == 'POST':
        return JsonResponse({'redirect': False})
    if request.user.is_authenticated:
        return redirect('home')

    # If request is post and user is not registered or logged in
    if request.method == 'POST' and not request.user.is_authenticated:

        # Verify the request data and register the user
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            return JsonResponse({'success': True, 'redirect': '/auth/login/'})
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


# Profile view

class ProfileView(LoginRequiredMixin, View):

    """
    View for users profile containing complaints outline and more.
    """

    template_name = 'profile.html'

    def get(self, request):

        """
        Render profile page with all users complaints and their status

        :param request:
        :return:
        """

        complaints = Complain.objects.filter(
            Q(user=request.user)
        )

        # If someone redirects to this page for opening a complaint
        complaint = request.GET.get('complaint_id')
        if complaint:
            complaint = Complain.objects.filter(pk=complaint).first()

        context = {
            'complaints': complaints,
            'complaints_count': len(complaints),
            'complaint': complaint
        }
        return render(request, self.template_name, context)