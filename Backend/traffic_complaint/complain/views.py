# Imports
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import PoliceStation, Attachment, Complain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

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


class ComplainWithAI(LoginRequiredMixin, View):

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


class ComplainView(LoginRequiredMixin, View):

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

        station_id = data.get('station')
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

                file_type = 'image'
                if not content_type.startswith('image/'):
                    file_type = 'video'

                # Creating attachment instance
                attachment = Attachment(complain=complain, file=uploaded_file, file_type=file_type)
                attachments.append(attachment)

        with transaction.atomic():
            try:
                # Bulk create attachments in a transaction
                Attachment.objects.bulk_create(attachments)
            except Exception as e:
                return JsonResponse({'message': 'An error occurred while creating attachments.', 'error': str(e)},
                                    status=500)

        return JsonResponse({'success': True, 'message': 'Complaint filed successfully!', 'complaint_id': complain.id})


class ComplainList(View):

    """
    View for listing out complains to normal users.
    """

    template_name = 'list_complaints.html'

    def get(self, request):

        """
        Return rendered list of complaints to normal users with filtering functionality

        :param request:
        :return:
        """

        # Filtering section
        search = request.GET.get('search', '')
        police_station = request.GET.get('station', None)

        complaints = Complain.objects.filter(
            Q(location__icontains=search) | Q(vehicle_number__icontains=search) |
            Q(complain_title__icontains=search) | Q(id__icontains=search)
        )

        if police_station:
            complaints = complaints.filter(
                Q(station__id=int(police_station))
            )

        # Pagination logic
        page = request.GET.get('page', 1)
        paginator = Paginator(complaints, 10)

        try:
            complaints_page = paginator.page(page)
        except PageNotAnInteger:
            # If the page is not an integer, deliver the first page
            complaints_page = paginator.page(1)
        except EmptyPage:
            # If the page is out of range, deliver the last page of results
            complaints_page = paginator.page(paginator.num_pages)

        # If someone redirects to this page for opening a complaint
        complaint = request.GET.get('complaint_id')
        if complaint:
            complaint = Complain.objects.filter(pk=complaint).first()

        stations = PoliceStation.objects.all()

        context = {
            'complaints': complaints_page,
            'complaint': complaint,
            'stations': stations
        }

        # Render the template with the paginated complaints and or complaint
        return render(request, self.template_name, context)

    def post(self, request, pk):

        """
        Update an complaint status

        :param request:
        :return:
        """

        if request.user.is_police_officer:
            data = request.POST
            complaint_id = pk
            status = data.get('status')

            complaint = Complain.objects.filter(pk=complaint_id).first()
            if complaint:
                complaint.status = int(status)
                complaint.save()

                return JsonResponse({"message": "Status updated successfully!"})
            return JsonResponse({"message": "No complaint found!"})

        return JsonResponse({"message": "You don't have permissions!"})

