# Generated by Django 3.2.18 on 2023-02-22 08:43

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_textblock_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textblock',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.lesson_image_file_path),
        ),
    ]
