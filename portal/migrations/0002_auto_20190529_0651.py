# Generated by Django 2.2.1 on 2019-05-29 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowers',
            options={'managed': False, 'verbose_name_plural': 'Borrowers'},
        ),
        migrations.AlterModelOptions(
            name='branches',
            options={'managed': False, 'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'managed': False, 'verbose_name_plural': 'Categories'},
        ),
    ]
