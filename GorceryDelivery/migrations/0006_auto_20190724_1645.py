# Generated by Django 2.2.2 on 2019-07-24 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GorceryDelivery', '0005_auto_20190710_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='GorceryDelivery.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='discounted_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
