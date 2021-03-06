# Generated by Django 2.1.7 on 2019-07-23 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capabilities', '0009_protectedcapability_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectedcapability',
            name='protected_resources',
            field=models.TextField(default='[["GET", "/some-url"]]', help_text='A JSON list of pairs containing HTTP method and URL.\n        It may contain [id] placeholders for wildcards\n        Example: [["GET","/api/task1"], ["POST","/api/task2/[id]"]]'),
        ),
    ]
