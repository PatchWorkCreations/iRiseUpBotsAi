# Generated by Django 4.2.11 on 2024-08-22 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_remove_emailcollection_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcollection',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254, unique=True),
        ),
    ]