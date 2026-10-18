from django.contrib import admin
from .models import Tag, Project, ProjectMetric, ArchitectureNode


class ProjectMetricInline(admin.TabularInline):
    model = ProjectMetric
    extra = 1


class ArchitectureNodeInline(admin.TabularInline):
    model = ArchitectureNode
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'color')
    list_filter = ('category',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'health_status', 'featured', 'order', 'github_stars', 'created_at')
    list_filter = ('featured', 'health_status', 'tags')
    search_fields = ('title', 'tagline', 'problem_statement')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectMetricInline, ArchitectureNodeInline]
    filter_horizontal = ('tags',)
