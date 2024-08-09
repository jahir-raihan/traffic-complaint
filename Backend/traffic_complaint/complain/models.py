import mimetypes
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PoliceStation(models.Model):

    """
    Model for storing police stations data
    """

    station_name = models.CharField(max_length=100)
    city = models.CharField(max_length=40)
    division = models.CharField(max_length=40)
    area = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.station_name} of {self.city}'


class Complain(models.Model):

    """
    Complaint model for storing complaints
    """

    COMPLAIN_STATUS = (
        (1, 'Pending'),
        (2, 'Investigating'),
        (3, 'Solved'),
        (4, 'Archived')
    )

    station = models.ForeignKey(PoliceStation, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    vehicle_number = models.CharField(max_length=10, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    complain_details = models.TextField(null=True, blank=True)
    complain_title = models.CharField(max_length=120, null=True, blank=True)
    status = models.SmallIntegerField(choices=COMPLAIN_STATUS, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Complaint ID {self.id}. Title: {self.complain_title}'


class Attachment(models.Model):

    """
    Attachment model for storing files
    """

    FILE_TYPE_CHOICES = [

        ('image', 'Image'),
        ('video', 'Video'),

    ]

    complain = models.ForeignKey(Complain, related_name='attachment', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='complain_files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)

    @property
    def is_image(self):
        return self.file_type == 'image'

    @property
    def is_video(self):
        return self.file_type == 'video'

    @property
    def content_type(self):
        mime_type, _ = mimetypes.guess_type(self.file.name)
        return mime_type
