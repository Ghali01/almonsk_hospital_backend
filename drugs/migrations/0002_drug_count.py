# Generated by Django 3.2.9 on 2021-12-01 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
