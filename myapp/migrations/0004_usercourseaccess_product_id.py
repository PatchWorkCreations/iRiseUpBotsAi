# Generated by Django 4.2.11 on 2024-12-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "myapp",
            "0003_rename_is_favorite_usercourseaccess_grace_period_enabled_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="usercourseaccess",
            name="product_id",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
