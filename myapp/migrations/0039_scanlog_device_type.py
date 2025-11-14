from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_alter_attendancelog_action_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanlog',
            name='device_type',
            field=models.CharField(
                choices=[
                    ('mobile', 'Mobile'),
                    ('tablet', 'Tablet'),
                    ('desktop', 'Desktop'),
                    ('bot', 'Bot'),
                    ('unknown', 'Unknown'),
                ],
                default='unknown',
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]

