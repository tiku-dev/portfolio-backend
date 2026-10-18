from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend & Architecture'),
        ('database', 'Databases & Caching'),
        ('devops', 'DevOps & Cloud'),
        ('frontend', 'Frontend & UI'),
        ('tools', 'Tools & Libraries'),
    ]

    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True, blank=True)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='backend')
    icon = models.CharField(max_length=64, blank=True, help_text="Lucide or Devicon identifier, e.g. 'si-django'")
    color = models.CharField(max_length=16, default='#092E20', help_text="Hex color code, e.g. #092E20")

    class Meta:
        ordering = ['category', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Project(models.Model):
    HEALTH_CHOICES = [
        ('healthy', 'Operational 🟢'),
        ('degraded', 'Degraded 🟡'),
        ('offline', 'Offline 🔴'),
        ('unknown', 'Unknown ⚪'),
    ]

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    tagline = models.CharField(max_length=255, help_text="One-sentence executive summary")
    problem_statement = models.TextField(help_text="The core engineering or business problem tackled")
    architecture_overview = models.TextField(help_text="Detailed explanation of system architecture, data flow, and trade-offs")
    key_achievements = models.JSONField(default=list, blank=True, help_text="List of technical wins (e.g. ['Sub-20ms P99 latency', 'Zero-downtime schema migrations'])")
    
    github_url = models.URLField(blank=True, default='')
    demo_url = models.URLField(blank=True, default='')
    health_check_url = models.URLField(blank=True, default='', help_text="Target URL for automated uptime probes")
    
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    featured = models.BooleanField(default=False, db_index=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    # Automated Sync Engine Fields
    health_status = models.CharField(max_length=16, choices=HEALTH_CHOICES, default='unknown')
    last_health_check = models.DateTimeField(null=True, blank=True)
    github_stars = models.PositiveIntegerField(default=0)
    github_forks = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectMetric(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='metrics')
    label = models.CharField(max_length=64, help_text="e.g. 'Latency Reduction', 'Throughput'")
    value = models.CharField(max_length=32, help_text="e.g. '65%', '15,000 req/sec'")
    description = models.CharField(max_length=255, blank=True, help_text="e.g. 'Achieved via Redis multi-level caching'")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.project.title} - {self.label}: {self.value}"


class ArchitectureNode(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='architecture_nodes')
    component_name = models.CharField(max_length=64, help_text="e.g. 'Postgres Read Replica', 'Celery Worker Pool'")
    role = models.CharField(max_length=255, help_text="e.g. 'Handles heavy analytical queries without loading primary DB'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title}: {self.component_name}"
