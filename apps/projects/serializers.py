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

    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), source='tags', required=False, write_only=True
    )
    metrics_data = serializers.ListField(
        child=serializers.DictField(), required=False, write_only=True
    )
    architecture_data = serializers.ListField(
        child=serializers.DictField(), required=False, write_only=True
    )

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
            'order',
            'tags',
            'tag_ids',
            'metrics',
            'metrics_data',
            'architecture_nodes',
            'architecture_data',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        metrics_data = validated_data.pop('metrics_data', [])
        architecture_data = validated_data.pop('architecture_data', [])
        tags = validated_data.pop('tags', None)

        project = Project.objects.create(**validated_data)

        if tags is not None:
            project.tags.set(tags)

        for m in metrics_data:
            ProjectMetric.objects.create(
                project=project,
                label=m.get('label') or m.get('metric_name', ''),
                value=m.get('value') or m.get('metric_value', ''),
                description=m.get('description') or m.get('metric_description', ''),
            )

        for a in architecture_data:
            ArchitectureNode.objects.create(
                project=project,
                component_name=a.get('component_name') or a.get('label', ''),
                role=a.get('role') or a.get('description', ''),
                order=a.get('order', 0),
            )

        return project

    def update(self, instance, validated_data):
        metrics_data = validated_data.pop('metrics_data', None)
        architecture_data = validated_data.pop('architecture_data', None)
        tags = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        if metrics_data is not None:
            instance.metrics.all().delete()
            for m in metrics_data:
                ProjectMetric.objects.create(
                    project=instance,
                    label=m.get('label') or m.get('metric_name', ''),
                    value=m.get('value') or m.get('metric_value', ''),
                    description=m.get('description') or m.get('metric_description', ''),
                )

        if architecture_data is not None:
            instance.architecture_nodes.all().delete()
            for a in architecture_data:
                ArchitectureNode.objects.create(
                    project=instance,
                    component_name=a.get('component_name') or a.get('label', ''),
                    role=a.get('role') or a.get('description', ''),
                    order=a.get('order', 0),
                )

        return instance

