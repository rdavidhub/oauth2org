# Generated by Django 2.2.13 on 2021-01-14 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientface_api', '0002_auto_20200827_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crosswalk',
            name='issuer',
            field=models.TextField(blank=True, default='', help_text='Usually an URL'),
        ),
    ]