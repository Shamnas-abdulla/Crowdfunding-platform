# Generated by Django 4.2.4 on 2023-09-02 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0003_users_signup_signup_password_signup_phone'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Signup',
            new_name='admin_Signup',
        ),
        migrations.RenameModel(
            old_name='Users_signup',
            new_name='user_signup',
        ),
    ]
