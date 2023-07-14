# Generated by Django 4.2.3 on 2023-07-14 06:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Dashboard", "0004_userprofile_profile_picture_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department_notice",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 11, 57, 2, 781396)
            ),
        ),
        migrations.AlterField(
            model_name="leaveapply",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 11, 57, 2, 781396)
            ),
        ),
        migrations.AlterField(
            model_name="notice_board",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 11, 57, 2, 781396)
            ),
        ),
        migrations.AlterField(
            model_name="paycheque",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 11, 57, 2, 781396)
            ),
        ),
        migrations.AlterField(
            model_name="paycheque",
            name="updated_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 11, 57, 2, 781396)
            ),
        ),
        migrations.AlterField(
            model_name="todaytasks",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 11, 57, 2, 781396)
            ),
        ),
    ]
