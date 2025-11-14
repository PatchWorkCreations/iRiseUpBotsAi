from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_scanlog_device_type'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE myapp_scanlog
                        ADD COLUMN IF NOT EXISTS enriched BOOLEAN
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunSQL(
                    sql="""
                        UPDATE myapp_scanlog
                        SET enriched = FALSE
                        WHERE enriched IS NULL
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE myapp_scanlog
                        ALTER COLUMN enriched SET DEFAULT FALSE,
                        ALTER COLUMN enriched SET NOT NULL
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='scanlog',
                    name='enriched',
                    field=models.BooleanField(default=False),
                ),
            ],
        ),
    ]

