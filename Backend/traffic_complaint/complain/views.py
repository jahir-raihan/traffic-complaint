# Imports

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# End Imports


class HomeView(View):

    """
    Home view with basic navigation logic
    """

    template_name = 'index.html'

    def get(self, request):

        """

        Render home page template and other user logical navigation

        :param request:
        :return HttpResponse:
        """

        return render(request, self.template_name, {})


class ListComplaint(View):

    """
    View to ist out complaints for normal users
    """

    template_name = 'list_complaints.html'

    def get(self, request):

        """
        Render complaints list with search and filtering functionality
        :param request:
        :return:
        """

        context = {

        }

        return render(request, self.template_name, context)

