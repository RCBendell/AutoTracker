# Generated by Django 3.1.6 on 2021-04-07 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0013_auto_20210406_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/uploaded_images/'),
        ),
    ]