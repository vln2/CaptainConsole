# Generated by Django 3.0.5 on 2020-05-13 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaptainConsole', '0006_auto_20200513_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cardCVC',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cardExp',
            field=models.CharField(max_length=4),
        ),
    ]
