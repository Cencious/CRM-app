# Generated by Django 4.1.4 on 2023-02-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]