# Generated by Django 4.0.4 on 2022-05-18 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RadioUniverse', '0003_remove_radiostation_banner_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiostation',
            name='town',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
