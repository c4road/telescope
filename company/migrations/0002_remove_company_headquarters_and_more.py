# Generated by Django 4.2.11 on 2025-03-30 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="headquarters",
        ),
        migrations.RemoveField(
            model_name="company",
            name="year_founded",
        ),
        migrations.AddField(
            model_name="company",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="employee_growth_1Y",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="employee_growth_2Y",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="employee_growth_6M",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="employee_locations",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="founded_year",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="headquarters_city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="industry",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="company",
            name="last_processed",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="company",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="total_employees",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
