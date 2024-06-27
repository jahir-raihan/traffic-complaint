from django.urls import path
from .views import HomeView, ListComplaint


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list-complaints', ListComplaint.as_view(), name='list_complaints_users')
]