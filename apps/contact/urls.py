from django.urls import path
from .views import ContactSubmissionView, InquiryListView

app_name = 'contact'

urlpatterns = [
    path('', ContactSubmissionView.as_view(), name='contact-submit'),
    path('inquiries/', InquiryListView.as_view(), name='inquiry-list'),
]

