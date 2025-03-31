import csv
import io
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from company.models import Company


class CompanyDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_import_company_data_csv(self):
        url = reverse("import_company_data")
        csv_data = """company_name,url,founded_year,total_employees,headquarters_city,employee_locations,employee_growth_2Y,employee_growth_1Y,employee_growth_6M,description,industry
CloudLogic Labs,https://www.cloudlogiclabs.com,2021,38,Boston (USA),"{""USA"": 32, ""Canada"": 3, ""UK"": 2, ""India"": 1}",85.2,38.6,19.8,"Project management platform with integrated resource allocation, subscription-based pricing with tiered plans",Software"""
        csv_file = io.StringIO(csv_data)
        response = self.client.post(url, {"file": csv_file}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(response.data["message"], "Successfully imported 1 records.")

    def test_import_company_data_json(self):
        url = reverse("import_company_data")
        json_data = [
            {
                "company_name": "CloudLogic Labs",
                "url": "https://www.cloudlogiclabs.com",
                "founded_year": 2021,
                "total_employees": 38,
                "headquarters_city": "Boston (USA)",
                "employee_locations": json.dumps(
                    {"USA": 32, "Canada": 3, "UK": 2, "India": 1}
                ),
                "employee_growth_2Y": "85.2",
                "employee_growth_1Y": "38.6",
                "employee_growth_6M": "19.8",
                "description": "Project management platform with integrated resource allocation, subscription-based pricing with tiered plans",
                "industry": "Software",
            }
        ]
        response = self.client.post(url, json_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(response.data["message"], "Successfully imported 1 records.")

    def test_get_companies(self):
        Company.objects.create(
            company_name="Test Company",
            url="https://www.test.com",
            total_employees=100,
            founded_year=2020,
            headquarters_city="New York",
            industry="Technology",
        )
        url = reverse("get_companies")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["company_name"], "Test Company")

    def test_process_company(self):
        company = Company.objects.create(
            company_name="Test Company",
            url="https://www.test.com",
            total_employees=50,
            founded_year=2020,
            headquarters_city="New York (USA)",
            industry="Software",
        )
        url = reverse("process_company")
        data = {
            "companies": ["https://www.test.com"],
            "rules": [
                {
                    "input": "total_employees",
                    "feature_name": "head_count_feature",
                    "operation": {"greater_than": 40},
                    "match": 1,
                    "default": 0,
                },
                {
                    "input": "company_age",
                    "feature_name": "age_feature",
                    "operation": {"less_than": 6},
                    "match": 1,
                    "default": 0,
                },
                {
                    "input": "is_usa_based",
                    "feature_name": "usa_based_feature",
                    "operation": {"equal": True},
                    "match": 1,
                    "default": 0,
                },
                {
                    "input": "is_saas",
                    "feature_name": "is_saas_feature",
                    "operation": {"equal": True},
                    "match": 1,
                    "default": 0,
                },
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Assert that the feature values are present in the response
        self.assertIn("head_count_feature", response.data[0])
        self.assertIn("age_feature", response.data[0])
        self.assertIn("usa_based_feature", response.data[0])
        self.assertIn("is_saas_feature", response.data[0])

        # Assert that the feature values are correct based on the rules
        self.assertEqual(response.data[0]["head_count_feature"], 1)
        self.assertEqual(
            response.data[0]["age_feature"], 1
        )  # Company age is 5 (2025 - 2020)
        self.assertEqual(response.data[0]["usa_based_feature"], 1)
        self.assertEqual(response.data[0]["is_saas_feature"], 1)
