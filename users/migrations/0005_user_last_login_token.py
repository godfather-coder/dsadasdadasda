# Generated by Django 4.2.7 on 2024-08-26 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_failed_listings_user_failed_listings_myhome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]