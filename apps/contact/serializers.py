from rest_framework import serializers
from .models import Inquiry


class InquiryCreateSerializer(serializers.ModelSerializer):
    # Honeypot field: Bots will fill this out, real humans won't see it
    website_url_hp = serializers.CharField(required=False, write_only=True, allow_blank=True)

    class Meta:
        model = Inquiry
        fields = ['id', 'name', 'email', 'subject', 'message', 'website_url_hp', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        honeypot = attrs.pop('website_url_hp', '')
        # If bot entered text in honeypot, mark as spam
        if honeypot:
            attrs['is_spam'] = True
            attrs['status'] = 'spam'
        return attrs

