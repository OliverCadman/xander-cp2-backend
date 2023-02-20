# Generated by Django 3.2.17 on 2023-02-20 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20230217_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textblock',
            name='exercise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_textblocks', to='core.exercise'),
        ),
        migrations.AlterField(
            model_name='textblock',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_textblocks', to='core.lesson'),
        ),
    ]
