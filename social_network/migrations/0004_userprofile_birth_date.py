# Generated by Django 5.0.12 on 2025-03-05 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0003_remove_postphoto_child_childphoto"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="birth_date",
            field=models.DateField(blank=True, null=True, verbose_name="Дата рождения"),
        ),
    ]
