# Generated by Django 4.0 on 2021-12-29 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connections', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blacklist',
        ),
        migrations.DeleteModel(
            name='Connection',
        ),
        migrations.RemoveField(
            model_name='edge_settings',
            name='edge_id',
        ),
        migrations.DeleteModel(
            name='Port_Punch',
        ),
        migrations.DeleteModel(
            name='Whitelist',
        ),
        migrations.DeleteModel(
            name='Edge',
        ),
        migrations.DeleteModel(
            name='Edge_Settings',
        ),
    ]
