# Generated by Django 3.0.5 on 2020-05-14 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CaptainConsole', '0011_auto_20200514_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CaptainConsole.Order'),
        ),
    ]