from datetime import date
from django.core.management.base import BaseCommand
from apps.projects.models import Tag, Project, ProjectMetric, ArchitectureNode
from apps.resume.models import BioProfile, Experience, Education


class Command(BaseCommand):
    help = 'Seeds the database with professional, standout portfolio case studies and resume data'

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding portfolio database...")

        # 1. Tags
        tags_data = [
            ("Django", "backend", "si-django", "#092E20"),
            ("Python", "backend", "si-python", "#3776AB"),
            ("PostgreSQL", "database", "si-postgresql", "#4169E1"),
            ("Redis", "database", "si-redis", "#DC382D"),
            ("Celery", "backend", "si-celery", "#37814A"),
            ("Docker", "devops", "si-docker", "#2496ED"),
            ("Kubernetes", "devops", "si-kubernetes", "#326CE5"),
            ("FastAPI", "backend", "si-fastapi", "#009688"),
            ("React", "frontend", "si-react", "#61DAFB"),
            ("TypeScript", "frontend", "si-typescript", "#3178C6"),
            ("GraphQL", "backend", "si-graphql", "#E10098"),
        ]

        tag_objs = {}
        for name, cat, icon, color in tags_data:
            t, _ = Tag.objects.get_or_create(
                name=name,
                defaults={'category': cat, 'icon': icon, 'color': color}
            )
            tag_objs[name] = t

        self.stdout.write(f"Created {len(tag_objs)} tags.")

        # 2. Bio Profile
        profile, _ = BioProfile.objects.get_or_create(
            full_name="Alex Mercer",
            defaults={
                "headline": "Senior Backend & Distributed Systems Engineer",
                "summary": (
                    "Backend Engineer specializing in resilient distributed systems, asynchronous event-driven pipelines, "
                    "and scalable API architectures using Django, PostgreSQL, and Redis. Passionate about system observability, "
                    "database query optimization, and engineering excellence."
                ),
                "email": "alex.mercer.eng@example.com",
                "location": "London, UK (Open to Global Remote)",
                "github_url": "https://github.com/octocat",
                "linkedin_url": "https://linkedin.com/in/octocat",
                "website_url": "https://alexmercer.dev",
                "available_for_hire": True,
                "availability_notice": "Available for Senior Backend / Staff roles"
            }
        )

        # 3. Case Study Projects
        p1, _ = Project.objects.get_or_create(
            slug="distributed-event-streamer",
            defaults={
                "title": "High-Throughput Distributed Event Streamer",
                "tagline": "Real-time webhook and audit stream processing 20M+ daily events with guaranteed idempotency",
                "problem_statement": (
                    "Third-party integrations caused burst traffic spikes that overwhelmed downstream relational databases, "
                    "leading to deadlocks and dropped event deliveries during peak hours."
                ),
                "architecture_overview": (
                    "Architected a decoupled ingestion pipeline using Django REST Framework, Redis Streams, and Celery worker pools. "
                    "Implemented distributed idempotency keys via Redis SETNX and dynamic backpressure throttling. "
                    "Analytical audit logs were batched into PostgreSQL using COPY streams."
                ),
                "key_achievements": [
                    "Zero event loss during downstream database maintenance windows",
                    "Maintained sub-25ms P99 API ingestion latency under 15,000 req/sec loads",
                    "Reduced database connection pool exhaustion by 90% via connection pooling"
                ],
                "github_url": "https://github.com/octocat/Spoon-Knife",
                "demo_url": "https://httpbin.org/status/200",
                "health_check_url": "https://httpbin.org/status/200",
                "featured": True,
                "order": 1,
                "health_status": "healthy",
                "github_stars": 342,
                "github_forks": 48
            }
        )
        p1.tags.set([tag_objs['Django'], tag_objs['Python'], tag_objs['Redis'], tag_objs['Celery'], tag_objs['PostgreSQL'], tag_objs['Docker']])

        ProjectMetric.objects.get_or_create(project=p1, label="Throughput", value="15,000 req/s", description="Peak ingestion capacity without event drops")
        ProjectMetric.objects.get_or_create(project=p1, label="P99 Latency", value="24ms", description="Measured across 50 million simulated payloads")
        ProjectMetric.objects.get_or_create(project=p1, label="Cost Reduction", value="40%", description="Optimized Redis memory footprint via hash sharding")

        ArchitectureNode.objects.get_or_create(project=p1, component_name="Ingestion Gateway", role="Fast stateless DRF endpoint performing token validation and HMAC signature checks", order=1)
        ArchitectureNode.objects.get_or_create(project=p1, component_name="Redis Stream Buffer", role="Decouples API ingestion from DB writes; buffers up to 500k burst messages", order=2)
        ArchitectureNode.objects.get_or_create(project=p1, component_name="Celery Worker Cluster", role="Consumes stream in batches of 100 with exponential backoff retries", order=3)
        ArchitectureNode.objects.get_or_create(project=p1, component_name="PostgreSQL Cluster", role="Primary write target with partition pruning by month", order=4)

        p2, _ = Project.objects.get_or_create(
            slug="multi-tenant-saas-core",
            defaults={
                "title": "Scalable Multi-Tenant SaaS Engine",
                "tagline": "Schema-isolated multi-tenant Django architecture with automated onboarding and tenant metering",
                "problem_statement": (
                    "Enterprise B2B clients required strict data isolation, compliance with data residency laws, "
                    "and dedicated resource allocation while maintaining a unified codebase."
                ),
                "architecture_overview": (
                    "Engineered schema-based multi-tenancy utilizing PostgreSQL schemas and custom Django middleware. "
                    "Built dynamic tenant routing, automated database schema migrations per tenant, and Stripe metered billing webhooks."
                ),
                "key_achievements": [
                    "Isolated 200+ distinct enterprise customer databases on a single cluster",
                    "Automated tenant provisioning pipeline in under 3.5 seconds",
                    "Zero cross-tenant data leakage verified by independent security audits"
                ],
                "github_url": "https://github.com/octocat/Hello-World",
                "demo_url": "https://httpbin.org/status/200",
                "health_check_url": "https://httpbin.org/status/200",
                "featured": True,
                "order": 2,
                "health_status": "healthy",
                "github_stars": 190,
                "github_forks": 27
            }
        )
        p2.tags.set([tag_objs['Django'], tag_objs['PostgreSQL'], tag_objs['Docker'], tag_objs['Kubernetes']])

        ProjectMetric.objects.get_or_create(project=p2, label="Provisioning Time", value="3.5s", description="From Stripe payment success to live tenant workspace")
        ProjectMetric.objects.get_or_create(project=p2, label="Active Tenants", value="200+", description="Running seamlessly on unified infrastructure")

        # 4. Experience
        e1, _ = Experience.objects.get_or_create(
            company="CloudScale Systems",
            role="Lead Backend Engineer",
            defaults={
                "location": "Remote",
                "start_date": date(2023, 1, 1),
                "is_current": True,
                "summary": "Leading the core backend team in designing scalable microservices and data pipelines.",
                "achievements": [
                    "Architected high-throughput ingestion microservice serving 10M+ daily events using Django and Redis",
                    "Spearheaded database query optimization initiative, reducing slow query occurrences by 75%",
                    "Mentored 6 backend engineers and established standard CI/CD and automated testing guidelines"
                ],
                "order": 1
            }
        )
        e1.tags.set([tag_objs['Django'], tag_objs['Python'], tag_objs['PostgreSQL'], tag_objs['Redis'], tag_objs['Docker']])

        e2, _ = Experience.objects.get_or_create(
            company="NexTech Solutions",
            role="Backend Software Engineer",
            defaults={
                "location": "London, UK",
                "start_date": date(2021, 3, 1),
                "end_date": date(2022, 12, 31),
                "is_current": False,
                "summary": "Built core REST APIs, payment integrations, and background worker queues.",
                "achievements": [
                    "Integrated Stripe Billing API with webhook signature verification and idempotent charge handling",
                    "Implemented Redis caching layer, dropping average response latency from 180ms to 28ms",
                    "Authored automated test suite reaching 88% branch coverage"
                ],
                "order": 2
            }
        )
        e2.tags.set([tag_objs['Django'], tag_objs['Python'], tag_objs['PostgreSQL'], tag_objs['Celery']])

        # 5. Education
        Education.objects.get_or_create(
            institution="University of Manchester",
            degree="B.Sc. (Hons)",
            field_of_study="Computer Science",
            defaults={
                "start_year": 2017,
                "end_year": 2020,
                "details": "First Class Honours. Focus on Distributed Systems and Software Engineering."
            }
        )

        self.stdout.write(self.style.SUCCESS("🎉 Successfully seeded portfolio with case studies, metrics, and resume!"))

