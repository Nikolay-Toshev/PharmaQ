# Generated by Django 5.1.3 on 2024-11-30 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_appuser_professional_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='is_approved',
        ),
    ]