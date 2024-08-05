from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Course
from django.template.loader import render_to_string
import os

@receiver(post_save, sender=Course)
def create_course_html(sender, instance, **kwargs):
    context = {'course': instance}
    html_content = render_to_string('myapp/course_templates/base_course_template.html', context)
    file_path = os.path.join('myapp/templates/myapp/generated_courses', f'{instance.title}.html')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(html_content)
