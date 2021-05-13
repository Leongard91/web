# Generated by Django 3.2 on 2021-05-13 13:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210513_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follow_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='_network_user_follow_to_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
