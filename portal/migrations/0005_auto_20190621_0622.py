# Generated by Django 2.2.1 on 2019-06-21 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20190621_0525'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FineReport',
            new_name='FineReportSummary',
        ),
        migrations.AlterModelTable(
            name='finereportsummary',
            table='fine_report_summary',
        ),
    ]
