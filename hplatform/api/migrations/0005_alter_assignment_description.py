# Generated by Django 5.1.7 on 2025-03-12 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_teacher_assignment_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
