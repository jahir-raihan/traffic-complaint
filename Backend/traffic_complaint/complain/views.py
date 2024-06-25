# Imports

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# End Imports


class HomeView(View):

    """
    Home view with basic navigation logic
    """

    def get(self, request):

        """

        Render home page template and other user logical navigations

        :param request:
        :return HttpResponse:
        """

        return HttpResponse("Yehee!")