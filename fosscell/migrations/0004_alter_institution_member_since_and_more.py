# Generated by Django 5.0.3 on 2024-03-06 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fosscell', '0003_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='member_since',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='pincode',
            field=models.IntegerField(),
        ),
    ]
