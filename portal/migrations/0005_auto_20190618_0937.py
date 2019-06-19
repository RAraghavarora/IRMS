# Generated by Django 2.2.1 on 2019-06-18 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_nodueaddressee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noduecertificate',
            name='borrower',
        ),
        migrations.AddField(
            model_name='noduecertificate',
            name='division',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noduecertificate',
            name='ic_number',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noduecertificate',
            name='mem_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noduecertificate',
            name='patron_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='noduecertificate',
            name='ref_no_date',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
