from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'is_spam', 'created_at')
    list_filter = ('status', 'is_spam')
    search_fields = ('name', 'email', 'message', 'subject')
    readonly_fields = ('created_at', 'ip_address')
