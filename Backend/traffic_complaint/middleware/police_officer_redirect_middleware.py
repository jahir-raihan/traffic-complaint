from django.shortcuts import redirect
from django.urls import reverse


class PoliceOfficerRedirectMiddleware:

    """
    Middleware to redirect users with 'is_police_officer' permission to a specific page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and has the 'is_police_officer' permission
        if request.user.is_authenticated and request.user.is_police_officer and not request.user.is_superuser and request.path != reverse('logout'):

            redirect_url = reverse('list_complaints_users')

            # Prevent infinite redirect loop
            if request.path != redirect_url:
                return redirect(redirect_url)

        response = self.get_response(request)
        return response
