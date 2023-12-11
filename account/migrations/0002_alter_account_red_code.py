# Generated by Django 4.2.7 on 2023-11-17 12:59

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='red_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh1234567890', length=10, max_length=20, prefix='', unique=True),
        ),
    ]
