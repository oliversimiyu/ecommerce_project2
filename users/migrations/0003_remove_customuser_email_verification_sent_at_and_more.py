# Generated by Django 5.0 on 2024-12-13 12:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_customuser_email_verification_sent_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="email_verification_sent_at",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="email_verification_token",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="email_verified",
        ),
    ]
