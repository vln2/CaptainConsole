# Generated by Django 3.0.6 on 2020-05-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaptainConsole', '0004_auto_20200511_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profile_picture',
            field=models.ImageField(blank=True, default='defaultuserimg.png', null=True, upload_to=''),
        ),
    ]
