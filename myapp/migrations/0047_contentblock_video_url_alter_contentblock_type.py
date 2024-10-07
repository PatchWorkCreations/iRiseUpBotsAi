# Generated by Django 4.2.11 on 2024-09-26 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0046_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentblock',
            name='video_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='type',
            field=models.CharField(choices=[('paragraph', 'Paragraph'), ('image', 'Image'), ('header', 'Header'), ('task', 'Task'), ('question', 'Question'), ('multiple_questions', 'Multiple Questions'), ('multiple_choice', 'Multiple Choice'), ('video_embed', 'Video Embed')], max_length=50),
        ),
    ]