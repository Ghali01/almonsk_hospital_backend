# Generated by Django 3.2.9 on 2021-12-02 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0004_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('O', 'Out'), ('E', 'Enter'), ('B', 'Back')], max_length=1)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='drugs.employee')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugs.drug')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='drugs.invoice')),
            ],
        ),
    ]
