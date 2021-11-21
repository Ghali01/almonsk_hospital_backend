from hospital.wsgi import application
from subprocess import check_output,call
from django.core.management import call_command
import sys

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=50)),
                ('fatherName', models.CharField(max_length=50)),
                ('secondName', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
    ]

def main():
    Migration('001i','doctors').apply()
    # stdout=sys.stdout
    # f=open('data.json','w',encoding='utf-8')
    # sys.stdout=f
    # call_command('dumpdata')
    # sys.stdout=stdout
    # f.close()
    # call_command('migrate')
    # call_command('loaddata','data.json')


if __name__ =='__main__':
    main()