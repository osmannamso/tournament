# Generated by Django 3.2.8 on 2021-10-10 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20211010_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='ends_at',
            field=models.DateTimeField(null=True),
        ),
    ]
