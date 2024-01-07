# Generated by Django 4.2.6 on 2024-01-04 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lesson",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.CharField(blank=True)),
                ("duration", models.IntegerField()),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                (
                    "subject",
                    models.IntegerField(
                        choices=[
                            (1, "Matematyka"),
                            (2, "Fizyka"),
                            (3, "Język angielski"),
                        ]
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Planned"), (2, "Completed"), (3, "Cancelled")]
                    ),
                ),
                ("calendar_meet_link", models.CharField(max_length=500)),
                ("cancelled_at", models.DateTimeField(blank=True, null=True)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_lessons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tutor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tutor_lessons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PriceList",
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
                (
                    "subject",
                    models.IntegerField(
                        choices=[
                            (1, "Matematyka"),
                            (2, "Fizyka"),
                            (3, "Język angielski"),
                        ]
                    ),
                ),
                ("hour_price", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "tutor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pricelist_set",
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "unique_together": {("tutor", "subject")},
            },
        ),
    ]
