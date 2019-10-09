# Generated by Django 2.2.2 on 2019-09-20 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GorceryDelivery', '0012_update_OrderItem_measureNpresentation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(default='Port-Harcourt', max_length=200)),
                ('phone_number', models.CharField(default='(+234)0000000000', max_length=16)),
                ('phone_number_2', models.CharField(default='(+234)0000000000', max_length=16, null=True)),
                ('address', models.TextField(default='Coca-cola junction, Trans-Amadi way')),
                ('email', models.EmailField(default='hero4barca@gmail.com', max_length=254)),
                ('site_domain', models.CharField(default='www.marketwoman.com.ng', max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='GorceryDelivery.Category'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='presentation',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='GorceryDelivery.Presentation'),
        ),
    ]