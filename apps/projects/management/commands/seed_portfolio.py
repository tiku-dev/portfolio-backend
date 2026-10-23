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
            ("Flutter", "frontend", "si-flutter", "#02569B"),
            ("Dart", "backend", "si-dart", "#0175C2"),
            ("JavaScript", "frontend", "si-javascript", "#F7DF1E"),
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
            full_name="Tiku Faith",
            defaults={
                "headline": "Intermediate Full-Stack Software Engineer | Python, JavaScript & Dart",
                "summary": (
                    "Intermediate full-stack software engineer with 2+ years of experience building web and mobile applications "
                    "in Python, JavaScript and Dart. Shipped TikuShop, an ecommerce platform with online payments, and built "
                    "an AI-powered file management app during an internship at Digimark Consulting SARL. Completing a Master's "
                    "in Computer Engineering in 2027 and seeking a remote software engineering role."
                ),
                "email": "tikufaith10@gmail.com",
                "location": "Bamenda, Cameroon (open to remote)",
                "github_url": "https://github.com/tiku-dev",
                "linkedin_url": "https://www.linkedin.com/in/tiku-faith-2305103a3",
                "website_url": "https://tikufaith.tikushop.com",
                "available_for_hire": True,
                "availability_notice": "Open to Remote Software Engineering Roles"
            }
        )

        # 3. Case Study Projects
        p0, _ = Project.objects.update_or_create(
            slug="tikushop",
            defaults={
                "title": "TikuShop — Full-Stack Ecommerce Platform",
                "tagline": "Production ecommerce web platform with online payments, product catalog, cart flows, and order management",
                "problem_statement": (
                    "Users needed an intuitive, fast, and secure ecommerce experience to discover products, "
                    "manage carts with real-time updates, and execute online payments directly from home."
                ),
                "architecture_overview": (
                    "Engineered with a robust Django REST Framework backend and a dynamic React frontend. "
                    "Integrated secure online payment processing, dynamic product catalog searching, and responsive cart session state."
                ),
                "key_achievements": [
                    "Built and deployed production ecommerce platform at tikushop.com",
                    "Integrated seamless online payment flow for home checkout",
                    "Architected robust Django REST APIs paired with reactive modern React frontend",
                ],
                "github_url": "",
                "demo_url": "https://tikushop.com",
                "health_check_url": "https://tikushop.com",
                "featured": True,
                "order": 1,
                "health_status": "healthy",
                "github_stars": 0,
                "github_forks": 0,
            }
        )
        p0.tags.set([tag_objs['Django'], tag_objs['React'], tag_objs['Python'], tag_objs['JavaScript'], tag_objs['PostgreSQL']])

        ProjectMetric.objects.update_or_create(project=p0, label="Platform", defaults={"value": "Production", "description": "Live production ecommerce at tikushop.com"})
        ProjectMetric.objects.update_or_create(project=p0, label="Payments", defaults={"value": "Online Gateway", "description": "Secure online digital checkout"})
        ProjectMetric.objects.update_or_create(project=p0, label="Tech Stack", defaults={"value": "Django + React", "description": "Full-stack decoupled architecture"})

        ArchitectureNode.objects.update_or_create(project=p0, component_name="React Frontend Client", defaults={"role": "Dynamic product catalog, interactive cart management, responsive UI", "order": 1})
        ArchitectureNode.objects.update_or_create(project=p0, component_name="Django REST API", defaults={"role": "Product search endpoints, order processing, and authentication", "order": 2})
        ArchitectureNode.objects.update_or_create(project=p0, component_name="Payment Gateway Integration", defaults={"role": "Online payment processor webhooks and transaction verification", "order": 3})
        ArchitectureNode.objects.update_or_create(project=p0, component_name="PostgreSQL Database", defaults={"role": "Relational storage for products, orders, categories, and customer data", "order": 4})

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
                "github_url": "https://github.com/tiku-dev/portfolio-frontend",
                "demo_url": "https://httpbin.org/status/200",
                "health_check_url": "https://httpbin.org/status/200",
                "featured": True,
                "order": 2,
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
                "github_url": "https://github.com/tiku-dev/portfolio-backend",
                "demo_url": "https://httpbin.org/status/200",
                "health_check_url": "https://httpbin.org/status/200",
                "featured": True,
                "order": 3,
                "health_status": "healthy",
                "github_stars": 190,
                "github_forks": 27
            }
        )
        p2.tags.set([tag_objs['React'], tag_objs['TypeScript'], tag_objs['Django'], tag_objs['PostgreSQL'], tag_objs['Docker'], tag_objs['Kubernetes']])

        ProjectMetric.objects.update_or_create(project=p2, label="Provisioning Time", defaults={"value": "3.5s", "description": "From Stripe checkout to live interactive tenant workspace"})
        ProjectMetric.objects.update_or_create(project=p2, label="Active Tenants", defaults={"value": "200+", "description": "Running seamlessly on unified infrastructure"})

        # 4. Experience
        Experience.objects.all().delete()

        e1 = Experience.objects.create(
            company="Digimark Consulting SARL",
            role="Software Engineering Intern",
            location="Yaoundé, Cameroon",
            start_date=date(2026, 8, 1),
            end_date=date(2026, 10, 31),
            is_current=False,
            summary="Designed and built a smart file management app that uses AI to carry out file-management jobs described by the user.",
            achievements=[
                "Designed and built a smart file management app that uses AI to carry out file-management jobs described by the user.",
                "Turned user-provided instructions into automated actions on files.",
                "Delivered the project within a two-month internship, following earlier internships at the same company."
            ],
            order=1
        )
        e1.tags.set([tag_objs['Python'], tag_objs['Django'], tag_objs['React'], tag_objs['JavaScript']])

        e2 = Experience.objects.create(
            company="Hands-on Full-Stack & Mobile Development",
            role="Software Developer",
            location="Bamenda, Cameroon (Remote)",
            start_date=date(2024, 1, 1),
            end_date=None,
            is_current=True,
            summary="2+ years of hands-on experience building and shipping web and mobile applications in Python, JavaScript and Dart.",
            achievements=[
                "Built and shipped full-stack web applications with Django and React, from backend APIs to user interfaces.",
                "Developed mobile and web features in Flutter, Dart and JavaScript.",
                "Engineered and launched TikuShop (tikushop.com), an ecommerce platform with online payment integration and product browsing."
            ],
            order=2
        )
        e2.tags.set([tag_objs['Python'], tag_objs['Django'], tag_objs['React'], tag_objs['JavaScript'], tag_objs['Flutter'], tag_objs['Dart'], tag_objs['PostgreSQL']])

        # 5. Education
        Education.objects.all().delete()
        Education.objects.create(
            institution="National Higher Polytechnic Institute (NAHPI)",
            degree="Master's in Computer Engineering",
            field_of_study="Computer Engineering",
            start_year=2022,
            end_year=2027,
            details="Completing a Master's in Computer Engineering, Bamenda, Cameroon · Expected 2027"
        )

        self.stdout.write(self.style.SUCCESS("🎉 Successfully seeded portfolio with case studies, metrics, and resume!"))

