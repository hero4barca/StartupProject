# Generated by Django 2.2.2 on 2020-02-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GorceryDelivery', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_type',
            new_name='transaction_reference',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='token_identifier',
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
