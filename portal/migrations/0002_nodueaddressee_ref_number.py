# Generated by Django 2.2.1 on 2019-06-19 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodueaddressee',
            name='ref_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
