# Generated by Django 3.1.6 on 2021-02-28 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=20)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('blog', models.TextField()),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=9)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='log.car')),
            ],
        ),
    ]