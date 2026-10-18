from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import BioProfile, Experience, Education
from .serializers import FullResumeSerializer
from .pdf_generator import generate_resume_pdf
from apps.telemetry.models import InteractionMetric


class ResumeDataView(APIView):
    """
    Returns full structured resume in JSON format.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        profile = BioProfile.objects.first()
        experiences = Experience.objects.prefetch_related('tags').all()
        education = Education.objects.all()

        data = {
            'profile': profile,
            'experiences': experiences,
            'education': education,
        }
        serializer = FullResumeSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResumePDFDownloadView(APIView):
    """
    Generates and streams a freshly compiled ATS-compliant PDF resume.
    Supports optional ?focus=backend or ?focus=devops parameter.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        focus = request.query_params.get('focus')

        # Log telemetry interaction
        try:
            InteractionMetric.objects.create(
                interaction_type='RESUME_DOWNLOAD',
                target_identifier=f"focus={focus or 'all'}"
            )
        except Exception:
            pass

        pdf_buffer = generate_resume_pdf(focus_category=focus)
        filename = f"Resume_{focus.capitalize() if focus else 'Backend'}.pdf"

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=filename,
            content_type='application/pdf'
        )
