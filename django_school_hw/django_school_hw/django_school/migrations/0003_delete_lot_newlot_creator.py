# Generated by Django 4.1.1 on 2023-01-10 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_school', '0002_newlot_delete_lot'),
    ]

    operations = [
        migrations.AddField(
            model_name='newlot',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]