from django.urls import path
from .views import ResumeDataView, ResumePDFDownloadView

app_name = 'resume'

urlpatterns = [
    path('', ResumeDataView.as_view(), name='resume-data'),
    path('pdf/', ResumePDFDownloadView.as_view(), name='resume-pdf-download'),
]

