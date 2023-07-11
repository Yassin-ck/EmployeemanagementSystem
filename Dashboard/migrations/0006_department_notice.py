# Generated by Django 4.2.3 on 2023-07-11 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0005_alter_notice_board_image_alter_notice_board_subject_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department_notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='department/')),
            ],
        ),
    ]