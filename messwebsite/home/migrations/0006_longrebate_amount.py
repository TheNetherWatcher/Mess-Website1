# Generated by Django 5.0.3 on 2024-04-16 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_email_longrebate_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='longrebate',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
