# Generated by Django 5.0.6 on 2024-07-03 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PoliceStation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("station_name", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=40)),
                ("division", models.CharField(max_length=40)),
                ("area", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Complain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "vehicle_number",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("contact", models.CharField(blank=True, max_length=15, null=True)),
                ("complain_details", models.TextField(blank=True, null=True)),
                (
                    "complain_title",
                    models.CharField(blank=True, max_length=120, null=True),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[
                            (1, "Pending"),
                            (2, "Investigating"),
                            (3, "Solved"),
                            (4, "Archived"),
                        ],
                        default=1,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="complain.policestation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="complain_files")),
                (
                    "file_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")], max_length=10
                    ),
                ),
                (
                    "complain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachment",
                        to="complain.complain",
                    ),
                ),
            ],
        ),
    ]
