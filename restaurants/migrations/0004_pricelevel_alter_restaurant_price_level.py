# Generated by Django 4.2.6 on 2023-10-26 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_alter_restaurant_latitude_alter_restaurant_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(help_text='Price level identifier (e.g., 1, 2, 3, 4, or 5)', unique=True)),
                ('description', models.CharField(help_text='Description of the price level', max_length=255)),
                ('min_price', models.DecimalField(decimal_places=2, help_text='Minimum price for this level', max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, help_text='Maximum price for this level', max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='price_level',
            field=models.ForeignKey(help_text='Price level of the restaurant', on_delete=django.db.models.deletion.PROTECT, to='restaurants.pricelevel'),
        ),
    ]
