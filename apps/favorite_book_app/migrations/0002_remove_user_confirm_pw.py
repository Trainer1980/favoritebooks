# Generated by Django 2.2 on 2020-01-25 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorite_book_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirm_pw',
        ),
    ]
