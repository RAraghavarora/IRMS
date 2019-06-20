# Generated by Django 2.2.1 on 2019-06-19 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20190619_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noduecertificate',
            name='addressee_content',
        ),
        migrations.AddField(
            model_name='noduecertificate',
            name='addressee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ndcs', to='portal.NoDueAddressee'),
        ),
    ]