# Generated by Django 4.2.7 on 2024-08-23 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_failed_listings_user_total_listings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='failed_listings',
            new_name='failed_listings_myhome',
        ),
        migrations.AddField(
            model_name='user',
            name='failed_listings_ss',
            field=models.JSONField(default=list),
        ),
    ]
