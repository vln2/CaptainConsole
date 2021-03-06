# Generated by Django 3.0.5 on 2020-05-14 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CaptainConsole', '0009_merge_20200514_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CaptainConsole.Order'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='CaptainConsole.Item', to='CaptainConsole.Product'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='cart',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CaptainConsole.Order'),
        ),
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CaptainConsole.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('order', 'product')},
        ),
    ]
