from django.urls import path
from .views import HomeView, ComplainList, ComplainWithAI, ComplainView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('list-complaints', ComplainList.as_view(), name='list_complaints_users'),
    path('complain-with-ai', ComplainWithAI.as_view(), name='complain_with_ai'),
    path('complain', ComplainView.as_view(), name='complain')
]