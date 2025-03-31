from django.db import models
from django.contrib.postgres.fields import JSONField


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    total_employees = models.IntegerField(blank=True, null=True)
    headquarters_city = models.CharField(max_length=255, blank=True, null=True)
    employee_locations = models.JSONField(blank=True, null=True)
    employee_growth_2Y = models.CharField(max_length=50, blank=True, null=True)
    employee_growth_1Y = models.CharField(max_length=50, blank=True, null=True)
    employee_growth_6M = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    imported_date = models.DateTimeField(auto_now_add=True)
    last_processed = models.DateTimeField(auto_now=True)

    company_age = models.IntegerField(blank=True, null=True)  # Add this line
    is_usa_based = models.BooleanField(blank=True, null=True)  # Add this line
    is_saas = models.BooleanField(blank=True, null=True)  # Add this line

    def __str__(self):
        return self.company_name
