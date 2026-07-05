# Generated manually to add choices for priority
from django.db import migrations, models


def add_priority_choices(apps, schema_editor):
    SupportTicket = apps.get_model('support', 'SupportTicket')
    # No data changes needed; this migration keeps schema in sync when field choices change.
    return

class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportticket',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Normal', 'Normal'), ('High', 'High'), ('Urgent', 'Urgent')], default='Normal', max_length=20),
        ),
    ]
