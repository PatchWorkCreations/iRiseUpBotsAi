# Generated by Django 4.2.11 on 2024-09-15 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_alter_forumpost_created_at_alter_transaction_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]