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
            ("React", "frontend", "si-react", "#61DAFB"),
            ("TypeScript", "frontend", "si-typescript", "#3178C6"),
            ("Next.js", "frontend", "si-nextdotjs", "#000000"),
            ("Tailwind CSS", "frontend", "si-tailwindcss", "#06B6D4"),
            ("Django", "backend", "si-django", "#092E20"),
            ("Python", "backend", "si-python", "#3776AB"),
            ("PostgreSQL", "database", "si-postgresql", "#4169E1"),
            ("Redis", "database", "si-redis", "#DC382D"),
            ("Celery", "backend", "si-celery", "#37814A"),
            ("Docker", "devops", "si-docker", "#2496ED"),
            ("Kubernetes", "devops", "si-kubernetes", "#326CE5"),
            ("FastAPI", "backend", "si-fastapi", "#009688"),
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
        profile, _ = BioProfile.objects.update_or_create(
            full_name="Alex Mercer",
            defaults={
                "headline": "Senior Full Stack & Systems Engineer",
                "summary": (
                    "Full Stack Engineer specializing in reactive web applications, resilient distributed systems, "
                    "and scalable API architectures using React, TypeScript, Tailwind CSS, Django, PostgreSQL, and Redis. "
                    "Passionate about end-to-end performance, fluid user interfaces, and engineering excellence."
                ),
                "email": "alex.mercer.eng@example.com",
                "location": "London, UK (Open to Global Remote)",
                "github_url": "https://github.com/octocat",
                "linkedin_url": "https://linkedin.com/in/octocat",
                "website_url": "https://alexmercer.dev",
                "available_for_hire": True,
                "availability_notice": "Available for Senior Full Stack & Lead Roles"
            }
        )

        # 3. Case Study Projects
        p1, _ = Project.objects.update_or_create(
            slug="collaborative-analytics-platform",
            defaults={
                "title": "Real-Time Collaborative Analytics Platform",
                "tagline": "Reactive data visualization dashboard with WebSocket synchronization and high-throughput ingestion",
                "problem_statement": (
                    "Distributed teams struggled with siloed analytics and out-of-sync dashboards during live product launches, "
                    "causing decision delays and conflicting metric interpretations."
                ),
                "architecture_overview": (
                    "Architected a responsive React 19 / TypeScript frontend with Tailwind CSS and WebSockets, "
                    "backed by Django REST Framework, Redis Streams, and Celery worker pools. Built optimistic UI updates "
                    "with live presence cursors and sub-25ms ingestion."
                ),
                "key_achievements": [
                    "Sub-25ms end-to-end telemetry propagation via WebSocket event pipelines",
                    "100/100 Lighthouse performance score with code-splitting and responsive mobile layout",
                    "Sustained 15,000 req/sec telemetry streams with zero message loss"
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
        p1.tags.set([tag_objs['React'], tag_objs['TypeScript'], tag_objs['Tailwind CSS'], tag_objs['Django'], tag_objs['Python'], tag_objs['Redis'], tag_objs['PostgreSQL'], tag_objs['Docker']])

        ProjectMetric.objects.update_or_create(project=p1, label="Throughput", defaults={"value": "15,000 req/s", "description": "Peak ingestion capacity without event drops"})
        ProjectMetric.objects.update_or_create(project=p1, label="UI P99 Latency", defaults={"value": "24ms", "description": "Measured across WebSocket live dashboard sessions"})
        ProjectMetric.objects.update_or_create(project=p1, label="Lighthouse Score", defaults={"value": "100/100", "description": "Optimized Core Web Vitals, accessibility, and PWA score"})

        ArchitectureNode.objects.update_or_create(project=p1, component_name="React 19 Client", defaults={"role": "Optimistic UI state, WebSocket client, dynamic theme & Tailwind layout", "order": 1})
        ArchitectureNode.objects.update_or_create(project=p1, component_name="Ingestion Gateway", defaults={"role": "Fast stateless DRF endpoint performing token validation and HMAC signature checks", "order": 2})
        ArchitectureNode.objects.update_or_create(project=p1, component_name="Redis Stream Buffer", defaults={"role": "Decouples API ingestion from DB writes; buffers burst messages and broadcasts WebSockets", "order": 3})
        ArchitectureNode.objects.update_or_create(project=p1, component_name="PostgreSQL Cluster", defaults={"role": "Primary write target with partition pruning by month", "order": 4})

        p2, _ = Project.objects.update_or_create(
            slug="multi-tenant-saas-workspace",
            defaults={
                "title": "Scalable Multi-Tenant SaaS Workspace",
                "tagline": "Full-stack enterprise SaaS workspace with interactive dashboard, tenant isolation, and automated billing",
                "problem_statement": (
                    "Enterprise B2B clients required strict data isolation, responsive mobile workspace management, "
                    "and metered billing while operating on a unified codebase."
                ),
                "architecture_overview": (
                    "Engineered an intuitive React + TypeScript client alongside schema-isolated PostgreSQL multi-tenancy in Django. "
                    "Included automated tenant provisioning, Stripe billing webhooks, and dark/light UI modes."
                ),
                "key_achievements": [
                    "Sub-3.5s automated tenant onboarding from checkout to live interactive dashboard",
                    "Isolated 200+ distinct enterprise customer workspaces on a single cluster",
                    "Zero cross-tenant data leakage verified by independent penetration audits"
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
        p2.tags.set([tag_objs['React'], tag_objs['TypeScript'], tag_objs['Django'], tag_objs['PostgreSQL'], tag_objs['Docker'], tag_objs['Kubernetes']])

        ProjectMetric.objects.update_or_create(project=p2, label="Provisioning Time", defaults={"value": "3.5s", "description": "From Stripe checkout to live interactive tenant workspace"})
        ProjectMetric.objects.update_or_create(project=p2, label="Active Tenants", defaults={"value": "200+", "description": "Running seamlessly on unified infrastructure"})

        # 4. Experience
        e1, _ = Experience.objects.update_or_create(
            company="CloudScale Systems",
            role="Lead Full Stack Engineer",
            defaults={
                "location": "Remote",
                "start_date": date(2023, 1, 1),
                "is_current": True,
                "summary": "Leading full stack development of reactive dashboards and scalable microservices with React 19, TypeScript, Django, and Redis.",
                "achievements": [
                    "Architected high-throughput ingestion microservice and real-time dashboard serving 10M+ daily events",
                    "Modernized client codebase to React 19 and Tailwind CSS, improving Core Web Vitals LCP by 45%",
                    "Mentored 6 full stack engineers and established standard CI/CD and automated testing guidelines"
                ],
                "order": 1
            }
        )
        e1.tags.set([tag_objs['React'], tag_objs['TypeScript'], tag_objs['Django'], tag_objs['Python'], tag_objs['PostgreSQL'], tag_objs['Redis'], tag_objs['Docker']])

        e2, _ = Experience.objects.update_or_create(
            company="NexTech Solutions",
            role="Full Stack Software Engineer",
            defaults={
                "location": "London, UK",
                "start_date": date(2021, 3, 1),
                "end_date": date(2022, 12, 31),
                "is_current": False,
                "summary": "Built responsive client interfaces, core REST APIs, payment integrations, and background worker queues.",
                "achievements": [
                    "Developed client-facing subscription portal in React with real-time Stripe payment status updates",
                    "Implemented Redis caching layer, dropping average API response latency from 180ms to 28ms",
                    "Authored automated frontend and backend test suites reaching 88% branch coverage"
                ],
                "order": 2
            }
        )
        e2.tags.set([tag_objs['React'], tag_objs['Django'], tag_objs['Python'], tag_objs['PostgreSQL'], tag_objs['Celery']])

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

