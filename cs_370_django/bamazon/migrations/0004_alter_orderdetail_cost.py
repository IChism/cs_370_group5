# Generated by Django 4.1.7 on 2023-05-02 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bamazon', '0003_cart_quantity_customer_prime_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
