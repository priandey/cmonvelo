# Generated by Django 3.1.2 on 2020-12-02 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikeowner', '0003_remove_owner_url_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='date_of_robbery',
            field=models.DateTimeField(null=True),
        ),
    ]
