# Generated by Django 4.2.5 on 2023-09-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0010_addcampaign_campaign_category_delete_admin_signup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addcampaign',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='addcampaign',
            name='phone',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
