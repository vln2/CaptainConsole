# Generated by Django 3.0.5 on 2020-05-12 22:09

from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('CaptainConsole', '0004_auto_20200511_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardNumber', django_cryptography.fields.encrypt(models.CharField(max_length=16))),
                ('cardName', models.CharField(max_length=255)),
                ('cardExp', models.DateField()),
                ('cardCVC', models.CharField(max_length=4)),
                ('status', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='CaptainConsole.Shipping'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='paymentInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CaptainConsole.Payment'),
        ),
    ]
