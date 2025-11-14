from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_alter_attendancelog_action_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE myapp_scanlog
                        ADD COLUMN IF NOT EXISTS device_type VARCHAR(20)
                        DEFAULT 'unknown'
                    """,
                    reverse_sql="""
                        ALTER TABLE myapp_scanlog
                        DROP COLUMN IF EXISTS device_type
                    """,
                ),
            ],
            state_operations=[
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
                ),
            ],
        ),
    ]

