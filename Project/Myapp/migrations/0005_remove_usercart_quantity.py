# Generated by Django 4.1.3 on 2023-03-29 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_alter_usercart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercart',
            name='quantity',
        ),
    ]