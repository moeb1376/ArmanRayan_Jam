# Generated by Django 2.0.2 on 2018-03-03 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180302_0342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ['competition_level']},
        ),
    ]