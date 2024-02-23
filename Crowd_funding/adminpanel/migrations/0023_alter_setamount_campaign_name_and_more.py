# Generated by Django 4.2.4 on 2024-01-06 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0022_setamount_campaign_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setamount',
            name='campaign_name',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpanel.addcampaign'),
        ),
        migrations.AlterField(
            model_name='setamount',
            name='charity_name',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpanel.addcharity'),
        ),
    ]