# Generated by Django 3.0.1 on 2020-01-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moonboard', '0003_auto_20200102_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='setyear',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]