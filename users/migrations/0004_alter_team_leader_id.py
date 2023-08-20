# Generated by Django 4.2.4 on 2023-08-20 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_task_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="leader_id",
            field=models.ForeignKey(
                limit_choices_to={"role": 1},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
