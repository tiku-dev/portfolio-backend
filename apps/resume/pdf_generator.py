import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import BioProfile, Experience, Education
from apps.projects.models import Tag


def generate_resume_pdf(focus_category=None):
    """
    Dynamically compiles a clean, ATS-compliant, professional PDF resume
    streamed directly into an in-memory byte stream.
    Supports filtering by skill category (e.g. 'backend', 'devops').
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#111827'),
        spaceAfter=2,
    )
    
    headline_style = ParagraphStyle(
        'DocHeadline',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=4,
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=10,
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=4,
        textTransform='uppercase'
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=4,
    )

    item_title = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#374151'),
        leftIndent=14,
        spaceAfter=2,
    )

    story = []

    profile = BioProfile.objects.first()
    if profile:
        story.append(Paragraph(profile.full_name, title_style))
        story.append(Paragraph(profile.headline, headline_style))
        contact_line = f"{profile.email} &bull; {profile.location}"
        if profile.github_url:
            contact_line += f" &bull; GitHub: {profile.github_url}"
        if profile.linkedin_url:
            contact_line += f" &bull; LinkedIn: {profile.linkedin_url}"
        story.append(Paragraph(contact_line, meta_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

        if profile.summary:
            story.append(Paragraph("Executive Summary", section_heading))
            story.append(Paragraph(profile.summary, body_style))
            story.append(Spacer(1, 6))

    # Experience section
    experiences = Experience.objects.prefetch_related('tags').all()
    if focus_category:
        experiences = experiences.filter(tags__category=focus_category).distinct()

    if experiences.exists():
        story.append(Paragraph("Professional Experience", section_heading))
        for exp in experiences:
            end_str = "Present" if exp.is_current else (exp.end_date.strftime("%b %Y") if exp.end_date else "")
            date_range = f"{exp.start_date.strftime('%b %Y')} - {end_str}"
            header_text = f"<b>{exp.role}</b> &mdash; <i>{exp.company}</i> ({exp.location})"
            
            # 2-column header with role/company on left and dates on right
            table_data = [[
                Paragraph(header_text, item_title),
                Paragraph(f"<para align='right'>{date_range}</para>", meta_style)
            ]]
            t = Table(table_data, colWidths=[380, 160])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(t)

            if exp.summary:
                story.append(Paragraph(exp.summary, body_style))

            if isinstance(exp.achievements, list):
                for ach in exp.achievements:
                    story.append(Paragraph(f"&bull; {ach}", bullet_style))

            # Tech stack tags
            tech_names = [t.name for t in exp.tags.all()]
            if tech_names:
                tech_line = f"<b>Technologies:</b> {', '.join(tech_names)}"
                story.append(Paragraph(tech_line, bullet_style))

            story.append(Spacer(1, 6))

    # Skills section
    tags_qs = Tag.objects.all()
    if focus_category:
        tags_qs = tags_qs.filter(category=focus_category)

    if tags_qs.exists():
        story.append(Paragraph("Technical Skills & Core Competencies", section_heading))
        categories = {}
        for tag in tags_qs:
            cat_name = tag.get_category_display()
            categories.setdefault(cat_name, []).append(tag.name)

        for cat, skills in categories.items():
            skill_text = f"<b>{cat}:</b> {', '.join(skills)}"
            story.append(Paragraph(skill_text, body_style))
        story.append(Spacer(1, 6))

    # Education section
    education = Education.objects.all()
    if education.exists():
        story.append(Paragraph("Education", section_heading))
        for edu in education:
            year_range = f"{edu.start_year} - {edu.end_year or 'Present'}"
            edu_text = f"<b>{edu.degree}</b> in {edu.field_of_study} &mdash; {edu.institution} ({year_range})"
            story.append(Paragraph(edu_text, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

