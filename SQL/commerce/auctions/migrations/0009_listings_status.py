# Generated by Django 3.2 on 2021-05-05 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210505_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'active'), ('s', 'sold'), ('d', 'deleted')], max_length=10, null=True),
        ),
    ]
