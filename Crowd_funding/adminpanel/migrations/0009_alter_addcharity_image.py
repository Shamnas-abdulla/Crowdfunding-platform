# Generated by Django 4.2.4 on 2023-09-07 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0008_addcharity_email_addcharity_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addcharity',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
