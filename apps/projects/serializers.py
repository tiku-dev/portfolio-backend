from rest_framework import serializers
from .models import Tag, Project, ProjectMetric, ArchitectureNode


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'category', 'icon', 'color']


class ProjectMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMetric
        fields = ['id', 'label', 'value', 'description']


class ArchitectureNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectureNode
        fields = ['id', 'component_name', 'role', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    metrics = ProjectMetricSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'tagline',
            'featured',
            'order',
            'github_url',
            'demo_url',
            'health_status',
            'github_stars',
            'tags',
            'metrics',
            'created_at',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    metrics = ProjectMetricSerializer(many=True, read_only=True)
    architecture_nodes = ArchitectureNodeSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'tagline',
            'problem_statement',
            'architecture_overview',
            'key_achievements',
            'github_url',
            'demo_url',
            'health_check_url',
            'health_status',
            'last_health_check',
            'github_stars',
            'github_forks',
            'featured',
            'tags',
            'metrics',
            'architecture_nodes',
            'created_at',
            'updated_at',
        ]

