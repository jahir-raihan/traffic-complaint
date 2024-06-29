# Imports

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import PoliceStation

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


class ComplainWithAI(View):

    """
    View for complaining using AI
    """

    template_name = 'complaint_with_ai.html'

    def get(self, request):

        """
        Render page and chat functionality to complain with ai

        :param request:
        :return:
        """

        context = {

        }

        return render(request, self.template_name, context)


class Complain(View):

    """
    View for complaining manually
    """

    template_name = 'complaint_form.html'

    def get(self, request):

        """
        Render page and chat functionality to complain with AI

        :param request:
        :return:
        """

        stations = PoliceStation.objects.all()

        context = {
            'stations': stations
        }

        return render(request, self.template_name, context)

    def post(self, request):

        """
        Store manual complaint submitted my user

        :param request:
        :return:
        """

        data = request.POST
        print(data)

