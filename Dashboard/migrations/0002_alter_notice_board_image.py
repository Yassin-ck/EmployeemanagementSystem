# Generated by Django 4.2.3 on 2023-07-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice_board',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]