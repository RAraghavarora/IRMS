# Generated by Django 2.2.1 on 2019-06-21 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20190621_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patroninfo',
            name='fine_ref_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='patroninfo',
            name='ndc_ref_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]