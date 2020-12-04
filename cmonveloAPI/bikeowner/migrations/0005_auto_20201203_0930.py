# Generated by Django 3.1.2 on 2020-12-03 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bikeowner', '0004_bike_date_of_robbery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bike',
            name='bike_model',
        ),
        migrations.AddField(
            model_name='details',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bikeowner.details', verbose_name='bikes'),
        ),
    ]