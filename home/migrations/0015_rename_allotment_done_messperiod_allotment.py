# Generated by Django 5.0.3 on 2024-05-06 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_messperiod_allotment_done_alter_cafeteria_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messperiod',
            old_name='allotment_done',
            new_name='allotment',
        ),
    ]
