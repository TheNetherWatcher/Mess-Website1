# Generated by Django 5.0.3 on 2024-04-16 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_longrebate_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='longrebate',
            old_name='email',
            new_name='student',
        ),
    ]