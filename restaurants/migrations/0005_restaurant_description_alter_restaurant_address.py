# Generated by Django 4.2.6 on 2023-10-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_pricelevel_alter_restaurant_price_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
