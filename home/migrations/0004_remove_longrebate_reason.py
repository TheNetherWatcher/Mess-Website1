# Generated by Django 5.0.3 on 2024-04-16 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_caterer_id_tobe_alloted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='longrebate',
            name='reason',
        ),
    ]