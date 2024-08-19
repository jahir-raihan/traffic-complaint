# Generated by Django 5.0.6 on 2024-08-09 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("complain", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment",
            name="complain",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attachment",
                to="complain.complain",
            ),
        ),
    ]
