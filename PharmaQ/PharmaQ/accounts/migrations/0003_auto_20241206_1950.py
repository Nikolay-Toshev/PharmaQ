from django.contrib.contenttypes.models import ContentType
from django.db import migrations

def create_users(apps, schema_editor):

    User = apps.get_model('accounts', 'AppUser')
    Group = apps.get_model('auth', 'Group')


    admin = User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin',
    )

    moderator = User.objects.create_user(
        username='moderator',
        email='moderator@admin.com',
        password='parolka123',
    )

    moderator.groups.add(Group.objects.get(name='site-moderator'))
    moderator.is_staff = True

    moderator.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20241204_2034'),
        ('consultation', '0002_auto_20241206_1907'),
    ]

    operations = [
        migrations.RunPython(create_users)
    ]
