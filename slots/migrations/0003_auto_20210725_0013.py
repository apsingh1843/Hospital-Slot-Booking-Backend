# Generated by Django 3.2.5 on 2021-07-24 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0002_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookings',
            name='requestCancel',
            field=models.CharField(choices=[('NO', 'Not Requested'), ('RE', 'Requested'), ('AC', 'Accepted'), ('DE', 'Declined')], default='NO', max_length=50),
        ),
    ]