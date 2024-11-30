from django.db import migrations, models
import uuid

def populate_security_codes(apps, schema_editor):
    Performer = apps.get_model('base', 'Perfomer')
    for performer in Performer.objects.filter(security_code__isnull=True):
        performer.security_code = str(uuid.uuid4())
        performer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_perfomer_security_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfomer',
            name='security_code',
            field=models.TextField(unique=True, null=True),  # Allow null temporarily
        ),
        migrations.RunPython(populate_security_codes),
        migrations.AlterField(
            model_name='perfomer',
            name='security_code',
            field=models.TextField(unique=True, null=False),  # Enforce non-null after populating
        ),
    ]
