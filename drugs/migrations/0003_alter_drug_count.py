# Generated by Django 3.2.9 on 2021-12-01 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0002_drug_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
