import shlex
import time
import requests
from django.utils import timezone
from apps.projects.models import Project, Tag
from apps.resume.models import BioProfile, Experience, Education
from apps.contact.models import Inquiry


class TerminalCommandDispatcher:
    """
    Parses and executes simulated developer CLI commands.
    Returns structured text and data for terminal UI frontends.
    """

    @classmethod
    def execute(cls, raw_command: str, client_ip: str = None) -> dict:
        trimmed = raw_command.strip()
        if not trimmed:
            return {"output": "", "status": "ok"}

        try:
            tokens = shlex.split(trimmed)
        except Exception:
            tokens = trimmed.split()

        cmd = tokens[0].lower()
        args = tokens[1:]

        handler = getattr(cls, f"cmd_{cmd}", None)
        if not handler:
            return {
                "output": f"zsh: command not found: {cmd}. Type 'help' for available commands.",
                "status": "error"
            }

        try:
            return handler(args, client_ip=client_ip)
        except Exception as e:
            return {"output": f"Error executing '{cmd}': {str(e)}", "status": "error"}

    @classmethod
    def cmd_help(cls, args, **kwargs):
        lines = [
            "===========================================================",
            "                  PORTFOLIO DEVELOPER CONSOLE              ",
            "===========================================================",
            "Available commands:",
            "  help                           Show this manual",
            "  whoami                         Display profile and availability",
            "  skills [--category=<cat>]      List skills (options: backend, database, devops, frontend)",
            "  skills --tree                  Render skills as an ASCII hierarchy",
            "  projects [--tag=<slug>]        List projects, live status, and repository stars",
            "  cat project <slug>             Print project case study & architecture breakdown",
            "  cat experience                 Print employment & engineering history",
            "  ping <slug>                    Ping live project demo & report real-time latency",
            "  contact <name> <email> <msg>   Send a direct message from the terminal",
            "  uptime                         Show system status & uptime indicator",
            "  clear                          Clear the terminal screen",
            "===========================================================",
        ]
        return {"output": "\n".join(lines), "status": "ok"}

    @classmethod
    def cmd_whoami(cls, args, **kwargs):
        profile = BioProfile.objects.first()
        if not profile:
            return {"output": "Guest Visitor (No BioProfile initialized yet)", "status": "ok"}
        
        status_line = "🟢 Open to opportunities" if profile.available_for_hire else "⚪ Currently unavailable"
        lines = [
            f"Name:         {profile.full_name}",
            f"Headline:     {profile.headline}",
            f"Location:     {profile.location}",
            f"Email:        {profile.email}",
            f"WhatsApp:     +237 671 486 996 (https://wa.me/237671486996)",
            f"Status:       {status_line} - {profile.availability_notice}",
            f"GitHub:       {profile.github_url or 'N/A'}",
            f"LinkedIn:     {profile.linkedin_url or 'N/A'}",
        ]
        return {"output": "\n".join(lines), "status": "ok"}

    @classmethod
    def cmd_skills(cls, args, **kwargs):
        if "--tree" in args:
            lines = ["└── Core Competencies"]
            categories = ['backend', 'database', 'devops', 'frontend', 'tools']
            for i, cat in enumerate(categories):
                tags = Tag.objects.filter(category=cat)
                if not tags.exists():
                    continue
                branch = "├── " if i < len(categories) - 1 else "└── "
                lines.append(f"    {branch}{cat.upper()}")
                tag_list = list(tags)
                for j, tag in enumerate(tag_list):
                    sub_branch = "│   ├── " if j < len(tag_list) - 1 else "│   └── "
                    lines.append(f"    │   {sub_branch}{tag.name}")
            return {"output": "\n".join(lines), "status": "ok"}

        # Filter by category if flag present
        category = None
        for arg in args:
            if arg.startswith("--category="):
                category = arg.split("=", 1)[1]

        qs = Tag.objects.all()
        if category:
            qs = qs.filter(category=category)

        if not qs.exists():
            return {"output": "No skills found matching filter.", "status": "ok"}

        lines = [f"{'SKILL':<24} {'CATEGORY':<20}"]
        lines.append("-" * 45)
        for tag in qs:
            lines.append(f"{tag.name:<24} {tag.get_category_display():<20}")

        return {"output": "\n".join(lines), "status": "ok"}

    @classmethod
    def cmd_projects(cls, args, **kwargs):
        qs = Project.objects.prefetch_related('tags').all()
        tag_filter = None
        for arg in args:
            if arg.startswith("--tag="):
                tag_filter = arg.split("=", 1)[1]

        if tag_filter:
            qs = qs.filter(tags__slug=tag_filter).distinct()

        if not qs.exists():
            return {"output": "No projects found matching criteria.", "status": "ok"}

        lines = [f"{'SLUG':<20} {'STARS':<6} {'STATUS':<15} {'TITLE'}"]
        lines.append("-" * 70)
        for p in qs:
            lines.append(f"{p.slug:<20} {p.github_stars:<6} {p.get_health_status_display():<15} {p.title}")

        return {"output": "\n".join(lines), "status": "ok"}

    @classmethod
    def cmd_cat(cls, args, **kwargs):
        if not args:
            return {"output": "Usage: cat project <slug>  OR  cat experience", "status": "error"}

        target = args[0].lower()
        if target == "project":
            if len(args) < 2:
                return {"output": "Usage: cat project <slug>", "status": "error"}
            slug = args[1]
            try:
                p = Project.objects.prefetch_related('tags', 'metrics', 'architecture_nodes').get(slug=slug)
            except Project.DoesNotExist:
                return {"output": f"Project '{slug}' not found. Run 'projects' to see valid slugs.", "status": "error"}

            lines = [
                f"# {p.title}",
                f"Tagline: {p.tagline}",
                f"Status:  {p.get_health_status_display()} | GitHub Stars: {p.github_stars}",
                "",
                "## Problem Statement",
                p.problem_statement,
                "",
                "## Architecture & Design Decisions",
                p.architecture_overview,
            ]
            if p.key_achievements:
                lines.append("\n## Key Achievements")
                for ach in p.key_achievements:
                    lines.append(f" - {ach}")

            if p.metrics.exists():
                lines.append("\n## Measurable Impact")
                for m in p.metrics.all():
                    lines.append(f" - {m.label}: {m.value} ({m.description})")

            return {"output": "\n".join(lines), "status": "ok"}

        elif target in ["experience", "resume"]:
            profile = BioProfile.objects.first()
            lines = [
                "===========================================================",
                "             TIKU FAITH – EXPERIENCE & RESUME              ",
                "===========================================================",
            ]
            if profile:
                lines.append(f"Name:     {profile.full_name}")
                lines.append(f"Location: {profile.location}")
                lines.append(f"Email:    {profile.email}")
                lines.append(f"WhatsApp: +237 671 486 996 (https://wa.me/237671486996)")
                lines.append(f"GitHub:   {profile.github_url or 'https://github.com/tiku-dev'}")
                if profile.linkedin_url:
                    lines.append(f"LinkedIn: {profile.linkedin_url}")
                if profile.summary:
                    lines.append(f"\n[Summary]\n{profile.summary}")

            exps = Experience.objects.prefetch_related('tags').all()
            if exps.exists():
                lines.append("\n[Work Experience]")
                for exp in exps:
                    end_str = "Present" if exp.is_current else (exp.end_date.strftime("%b %Y") if exp.end_date else "")
                    loc_str = f", {exp.location}" if exp.location else ""
                    lines.append(f"\n▶ {exp.role} @ {exp.company}{loc_str}")
                    lines.append(f"  Duration: {exp.start_date.strftime('%b %Y')} – {end_str}")
                    if exp.summary:
                        lines.append(f"  Summary:  {exp.summary}")
                    if isinstance(exp.achievements, list):
                        for ach in exp.achievements:
                            lines.append(f"  • {ach}")
            else:
                lines.append("\nNo experience records found.")

            edus = Education.objects.all()
            if edus.exists():
                lines.append("\n[Education]")
                for edu in edus:
                    end_str = f"Expected {edu.end_year}" if edu.end_year and edu.end_year > 2024 else (str(edu.end_year) if edu.end_year else "Present")
                    degree_str = edu.degree if edu.field_of_study in edu.degree else f"{edu.degree} in {edu.field_of_study}"
                    lines.append(f"▶ {degree_str}")
                    lines.append(f"  {edu.institution} ({end_str})")
                    if edu.details:
                        lines.append(f"  {edu.details}")

            lines.append("===========================================================")
            return {"output": "\n".join(lines), "status": "ok"}

        return {"output": f"File '{target}' not found.", "status": "error"}

    @classmethod
    def cmd_experience(cls, args, **kwargs):
        return cls.cmd_cat(["experience"], **kwargs)

    @classmethod
    def cmd_resume(cls, args, **kwargs):
        return cls.cmd_cat(["resume"], **kwargs)

    @classmethod
    def cmd_ping(cls, args, **kwargs):
        if not args:
            return {"output": "Usage: ping <project-slug>", "status": "error"}
        slug = args[0]
        try:
            project = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return {"output": f"Host '{slug}' unknown. Run 'projects' to view projects.", "status": "error"}

        target_url = project.health_check_url or project.demo_url
        if not target_url:
            return {"output": f"No live URL configured for '{slug}'.", "status": "ok"}

        try:
            start = time.perf_counter()
            resp = requests.get(target_url, timeout=5)
            latency = round((time.perf_counter() - start) * 1000, 2)
            project.health_status = 'healthy' if 200 <= resp.status_code < 400 else 'degraded'
            project.last_health_check = timezone.now()
            project.save(update_fields=['health_status', 'last_health_check'])
            return {
                "output": f"PING {target_url}\nStatus: {resp.status_code} {resp.reason}\nLatency: {latency}ms\nState: {project.get_health_status_display()}",
                "status": "ok"
            }
        except Exception as exc:
            project.health_status = 'offline'
            project.last_health_check = timezone.now()
            project.save(update_fields=['health_status', 'last_health_check'])
            return {"output": f"PING {target_url} FAILED: {str(exc)}", "status": "error"}

    @classmethod
    def cmd_contact(cls, args, client_ip=None, **kwargs):
        if len(args) < 3:
            return {
                "output": 'Usage: contact "<your name>" "<your email>" "<your message>"',
                "status": "error"
            }
        name, email, message = args[0], args[1], " ".join(args[2:])
        Inquiry.objects.create(
            name=name[:128],
            email=email[:128],
            subject="CLI Terminal Message",
            message=message,
            ip_address=client_ip
        )
        return {
            "output": f"Transmission received, {name}! Your message was logged successfully to the backend.",
            "status": "ok"
        }

    @classmethod
    def cmd_uptime(cls, args, **kwargs):
        return {
            "output": "System Status: OPERATIONAL 🟢 | Services: Django 5, PostgreSQL, Redis, Celery",
            "status": "ok"
        }

    @classmethod
    def cmd_clear(cls, args, **kwargs):
        return {"output": "", "status": "clear"}

