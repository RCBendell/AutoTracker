# Generated by Django 3.1.6 on 2021-04-07 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0012_entry_update_mileage'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='fyle',
            field=models.FileField(blank=True, null=True, upload_to='media/entry_files/'),
        ),
        migrations.AddField(
            model_name='entry',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/entry_images/'),
        ),
    ]
