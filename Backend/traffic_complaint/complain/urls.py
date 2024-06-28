from django.urls import path
from .views import HomeView, ListComplaint, ComplainWithAI, Complain


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list-complaints', ListComplaint.as_view(), name='list_complaints_users'),
    path('complain-with-ai', ComplainWithAI.as_view(), name='complain_with_ai'),
    path('complain', Complain.as_view(), name='complain')
]