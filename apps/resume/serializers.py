from rest_framework import serializers
from .models import BioProfile, Experience, Education
from apps.projects.serializers import TagSerializer


class BioProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BioProfile
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = [
            'id',
            'company',
            'role',
            'location',
            'start_date',
            'end_date',
            'is_current',
            'summary',
            'achievements',
            'tags',
            'order',
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class FullResumeSerializer(serializers.Serializer):
    profile = BioProfileSerializer()
    experiences = ExperienceSerializer(many=True)
    education = EducationSerializer(many=True)

