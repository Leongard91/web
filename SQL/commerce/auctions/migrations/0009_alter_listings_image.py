# Generated by Django 3.2 on 2021-05-03 09:21

import auctions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listings_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=auctions.models.Listings.user_directory_path, validators=[auctions.models.Listings.validate_file_extension]),
        ),
    ]
