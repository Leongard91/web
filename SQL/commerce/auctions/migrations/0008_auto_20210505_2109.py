# Generated by Django 3.2 on 2021-05-05 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listings_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='listings',
            name='in_users_watchlists',
            field=models.ManyToManyField(blank=True, related_name='listings_in_watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listings',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_actions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings_from_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='listings_on_category', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.URLField(),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_from_user', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_on_listing', to='auctions.listings')),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids_from_user', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids_on_listing', to='auctions.listings')),
            ],
        ),
    ]
