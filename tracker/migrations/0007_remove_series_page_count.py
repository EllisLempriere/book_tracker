# Generated by Django 5.0.2 on 2024-02-21 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_finishedread_inprogressread_series_seriesbook_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='page_count',
        ),
    ]
