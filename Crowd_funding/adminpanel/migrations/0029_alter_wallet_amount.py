# Generated by Django 4.2.4 on 2024-01-12 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0028_rename_autodedut_autodeduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]