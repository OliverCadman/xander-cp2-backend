# Generated by Django 3.2.16 on 2023-01-26 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=255)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='core.language')),
            ],
        ),
    ]
