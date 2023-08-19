# Generated by Django 4.2.4 on 2023-08-18 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teammember",
            name="user_id",
            field=models.ForeignKey(
                limit_choices_to=models.Q(("role__in", [0])),
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]