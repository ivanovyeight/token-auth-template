# Generated by Django 3.1.6 on 2021-02-09 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='user_id',
            new_name='user',
        ),
    ]
