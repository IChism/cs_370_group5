# Generated by Django 4.1.7 on 2023-04-10 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bamazon', '0002_media_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='prime_user',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='stars',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
