# Generated by Django 4.2.3 on 2023-07-14 14:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Dashboard", "0004_alter_department_notice_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department_notice",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 20, 11, 15, 910241)
            ),
        ),
        migrations.AlterField(
            model_name="leaveapply",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 20, 11, 15, 910241)
            ),
        ),
        migrations.AlterField(
            model_name="notice_board",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 20, 11, 15, 910241)
            ),
        ),
        migrations.AlterField(
            model_name="todaytasks",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 7, 14, 20, 11, 15, 910241)
            ),
        ),
    ]