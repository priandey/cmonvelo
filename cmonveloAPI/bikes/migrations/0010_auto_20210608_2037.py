# Generated by Django 3.1.8 on 2021-06-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0009_auto_20210607_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='picture',
            field=models.ImageField(blank=True, default='bikes/default.jpg', max_length=255, null=True, upload_to='bikes/'),
        ),
    ]
