# Generated by Django 5.0.3 on 2024-03-11 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fosscell', '0019_institution_fossadvisor_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='category',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='university',
        ),
        migrations.RemoveField(
            model_name='members',
            name='uid',
        ),
        migrations.DeleteModel(
            name='FossAdvisor',
        ),
        migrations.DeleteModel(
            name='Institution',
        ),
        migrations.DeleteModel(
            name='Members',
        ),
    ]