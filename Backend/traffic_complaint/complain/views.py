# Imports
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import PoliceStation, Attachment, Complain


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


class ComplainView(View):

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

        station_id = data.get('police_station')
        police_station = None
        if station_id:
            police_station = PoliceStation.objects.get(pk=station_id)

        complain = Complain(
            location=data.get('location'),
            vehicle_number=data.get('vehicle_number'),
            contact=data.get('contact'),
            complain_details=data.get('complain_details'),
        )

        if police_station:
            complain.station = police_station

        complain.complain_title = 'some generated complaint title'
        complain.save()

        attachments = []
        for field_name, files in request.FILES.lists():  # `lists()` to handle multiple files
            for uploaded_file in files:
                content_type = uploaded_file.content_type
                if not content_type.startswith('image/') and not content_type.startswith('video/'):
                    return JsonResponse(
                        {"message": f'Invalid file type for field "{field_name}": {content_type}'},
                        status=400
                    )

                # Creating attachment instance
                attachment = Attachment(complain=complain, file=uploaded_file)
                attachments.append(attachment)

        with transaction.atomic():
            try:
                # Bulk create attachments in a transaction
                Attachment.objects.bulk_create(attachments)
            except Exception as e:
                return JsonResponse({'message': 'An error occurred while creating attachments.', 'error': str(e)},
                                    status=500)

        return JsonResponse({'success': True, 'message': 'Complaint filed successfully!'})

