# Generated by Django 3.2.18 on 2023-02-21 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20230221_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textblock',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
