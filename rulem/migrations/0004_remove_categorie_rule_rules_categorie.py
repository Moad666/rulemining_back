# Generated by Django 4.1.7 on 2024-07-05 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rulem', '0003_categorie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorie',
            name='rule',
        ),
        migrations.AddField(
            model_name='rules',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rulem.categorie'),
        ),
    ]
