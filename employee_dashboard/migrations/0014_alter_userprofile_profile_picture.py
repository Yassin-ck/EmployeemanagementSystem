# Generated by Django 4.2.3 on 2023-07-20 09:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee_dashboard", "0013_alter_userprofile_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_picture",
            field=models.ImageField(
                default="userprofile/default.profilepicture.jp",
                upload_to="userprofile/",
            ),
        ),
    ]