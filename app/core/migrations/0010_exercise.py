# Generated by Django 3.2.17 on 2023-02-08 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20230208_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=255)),
                ('starter_code', models.FileField(upload_to='exercises/starter_code')),
                ('started_code_filename', models.CharField(max_length=255)),
                ('expected_outcome', models.FileField(upload_to='exercises/expected_outcomes')),
                ('expected_outcome_filename', models.CharField(max_length=255)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_exercises', to='core.topic')),
            ],
        ),
    ]
