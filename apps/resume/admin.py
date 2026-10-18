from django.contrib import admin
from .models import BioProfile, Experience, Education


@admin.register(BioProfile)
class BioProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'headline', 'email', 'available_for_hire')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current', 'company')
    search_fields = ('role', 'company', 'summary')
    filter_horizontal = ('tags',)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'field_of_study', 'institution', 'start_year', 'end_year')
    search_fields = ('institution', 'degree', 'field_of_study')
