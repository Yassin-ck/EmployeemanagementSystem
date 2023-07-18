# Generated by Django 4.2.3 on 2023-07-18 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("employee_dashboard", "0007_alter_paycheque_allowances_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="todaytasks",
            name="notice_board",
        ),
        migrations.AddField(
            model_name="department_notice",
            name="assigned_to",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="todaytasks",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
