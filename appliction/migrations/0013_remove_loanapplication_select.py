# Generated by Django 3.2.9 on 2021-11-20 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appliction', '0012_loanapplication_select'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapplication',
            name='select',
        ),
    ]