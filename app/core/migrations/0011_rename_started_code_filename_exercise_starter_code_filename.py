# Generated by Django 3.2.17 on 2023-02-08 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_exercise'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='started_code_filename',
            new_name='starter_code_filename',
        ),
    ]
