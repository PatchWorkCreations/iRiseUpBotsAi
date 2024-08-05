# myapp/management/commands/regenerate_course_html.py

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
import os
from myapp.models import Course

class Command(BaseCommand):
    help = 'Regenerate HTML files for all courses'

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()
        course_html_dir = os.path.join(settings.BASE_DIR, 'customadmin/templates/customadmin/course_templates')
        if not os.path.exists(course_html_dir):
            os.makedirs(course_html_dir)

        for course in courses:
            file_path = os.path.join(course_html_dir, f'course_{course.id}.html')
            html_content = render_to_string('customadmin/course_templates/base_course_template.html', {'course': course})
            with open(file_path, 'w') as html_file:
                html_file.write(html_content)
            self.stdout.write(self.style.SUCCESS(f'Successfully generated HTML for course {course.id}'))
