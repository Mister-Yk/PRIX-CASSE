# Generated by Django 5.0.7 on 2024-07-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]