# Generated by Django 4.2.7 on 2023-11-20 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0007_alter_account_account_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=15, max_length=20, prefix='TRN', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(choices=[('Failed', 'Failed'), ('Completed', 'Completed'), ('Pending', 'Pending'), ('Processing', 'Processing'), ('Request_Sent', 'Request_Sent'), ('Request_Settled', 'Request Settled'), ('Request_Processing', 'Request Processing')], default='pending', max_length=100)),
                ('transaction_type', models.CharField(choices=[('Transfer', 'Transfer'), ('Recieved', 'Recieved'), ('Withdraw', 'Withdraw'), ('Refund', 'Refund'), ('Request', 'Payment Request'), ('None', 'None')], default='none', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reciever', to=settings.AUTH_USER_MODEL)),
                ('reciever_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reciever_account', to='account.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('sender_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_account', to='account.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
