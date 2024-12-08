from django.db import migrations

def generate_groups(apps, schema_editor):

    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name="patient")
    Group.objects.get_or_create(name="pharmacist")
    Group.objects.get_or_create(name="site-moderator")

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_groups)
    ]
