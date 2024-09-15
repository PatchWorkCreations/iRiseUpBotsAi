# Generated by Django 4.2.11 on 2024-09-11 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0037_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(blank=True, max_length=50, null=True)),
                ('question_content', models.TextField(blank=True, null=True)),
                ('user_answer', models.TextField(blank=True, null=True)),
                ('correct_answer', models.TextField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('answered_on', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.lesson')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]