# Imports
import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import View

from decouple import config
from .helper.helpers import to_markdown
from .models import PoliceStation, Attachment, Complain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

import google.generativeai as genai
from django.core.cache import cache
from PIL import Image
import io
from .helper.helpers import extract_images

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
        :return HTTPResponse:
        """

        context = {}

        return render(request, self.template_name, context)

    def get_requirements(self, attached_text: str) -> str:

        """
        Return the requirements text containing commands

        :return string:
        """

        requirements = ("Generate a complaint out of the texts you've received and the chat you had with me. And the "
                        "Images / Videos I gave. "
                        "The complaint should contain fields including [location, vehicle_number[optional], "
                        "complain_details, complain_title, complete_status]. And if any field is missing you may set"
                        "the complete status false and add a new field of list named: missing_fields  containing "
                        "all the missing fields. And the output format should be in JSON") + attached_text

        return requirements

    def generate_complaint(self, chat, user):
        """
        Generate the final complaint in json format to store in the database

        :param chat:
        :param user:
        :return:
        """

        requirements = self.get_requirements("Avoid json prefix as it throws error while converting to native"
                                             "python dict object")

        response = {}
        missing_fields = []
        status = True
        complaint_id = None

        for _ in range(3):
            try:
                message = chat.send_message(requirements)
                response = json.loads(message.text)
                missing_fields = response['missing_fields'] if 'missing_fields' in response else []
                status = response['complete_status']

                break
            except:
                requirements = self.get_requirements("Please generate the complaint again in JSON format without"
                                                     "using json prefix , because it throws JSONEncode error while"
                                                     "converting to native python dict object.")

        if status:
            # Create compliant object here

            complaint = Complain(
                location=response['location'],
                vehicle_number=response['vehicle_number'],
                complain_details=response['complain_details'],
                complain_title=response['complain_title'],
                user=user
            )

            police_station = PoliceStation.objects.filter(
                Q(station_name__icontains=response['location']) |
                Q(city__icontains=response['location']) |
                Q(division__icontains=response['location']) |
                Q(area__icontains=response['location'])
            ).first()

            complaint.station = police_station
            complaint.save()
            complaint_id = complaint.id

            # Link all attachments so far
            attachment_id_cache_key = f'attachment_cache_{user.id}'
            cached_data = cache.get(attachment_id_cache_key)

            for a_id in cached_data:
                attachment_data = Attachment.objects.get(id=a_id)
                attachment_data.complain = complaint
                attachment_data.save()

            cache.set(attachment_id_cache_key, [], 10)
            cache.set(f'default_cache_key_{user.id}', [], 10)

        return complaint_id, status, missing_fields

    def post(self, request):

        """
        Handle chat with gemini for user to complaint without filling out form

        :param request:
        :return:
        """

        data = request.POST
        file = request.FILES

        GOOGLE_API_KEY = config('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-1.5-flash')
        cache_key = f'default_cache_key_{request.user.id}'
        cached_chat_data = cache.get(cache_key)

        if cached_chat_data:
            chat = model.start_chat(history=cached_chat_data['history'])
        else:
            chat = model.start_chat(history=[])
            cache.set('default_cache_key', {'history': chat.history}, 60 * 20)

        if data.get('submit', 'false') == 'true':
            complaint_id, status, fields_name = self.generate_complaint(chat, request.user)

            if not status:
                return JsonResponse(
                    {
                        "response": f"Please provide some more information on these fields: {fields_name}",
                        'status': status,
                        'complaint_id': complaint_id
                    }
                )
            else:

                return JsonResponse(
                    {
                        "response": f"Thank you for your time. Your complaint has been registered! You will be"
                                    f" redirected to the complaint shortly!",
                        'status': status,
                        'complaint_id': complaint_id

                    }
                )

        requirements = self.get_requirements(
             "If any field data is missing,"
             "you should ask for it first before response as json format, and don't ask"
             " for title and details you can generate by analysing the image"
             " then when I provide the data you can generate "
             "the json not before that!. If a image is provided you should analyse"
             " the image for "
             "kind of violation it is making, and the risk it's making for others,"
             " vehicle number and"
             "generate the complaint details and title on your own. I repeat if any "
             "field is missing, first ask for the fields without responding in json."
        )

        if 'file' in file:
            # Open the image using PIL
            image = Image.open(file.get('file'))
            attachment = Attachment.objects.create(file=file.get('file'), file_type='image')
            attachment.save()

            attachment_id_cache_key = f'attachment_cache_{request.user.id}'
            cached_data = cache.get(attachment_id_cache_key)
            if cached_data:
                cached_data.append(attachment.id)
            else:
                cached_data = [attachment.id]

            cache.set(attachment_id_cache_key, cached_data, 60*10)

            # Create the message to send with the image and text
            message = chat.send_message([
                image,
                data.get('chat_text') + requirements
            ])
        else:
            message = chat.send_message(data.get('chat_text') + requirements)

        # Update the cache with the new chat history
        cache.set(cache_key, {'history': chat.history}, 60 * 10)

        return JsonResponse({"response": message.text, 'status': False})


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

