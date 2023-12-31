# Generated by Django 4.2.7 on 2023-11-22 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_alter_useraddress_location"),
        ("property", "0003_alter_property_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyaddress",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="user.location"
            ),
        ),
    ]
