# Generated by Django 4.2.17 on 2025-03-02 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_carhistory_image_entry_plate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="carhistory",
            name="usage_time",
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="carhistory",
            name="created_date",
            field=models.DateTimeField(
                verbose_name=datetime.datetime(
                    2025, 3, 2, 20, 15, 28, 265511, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
