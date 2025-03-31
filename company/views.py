import csv
import io
import json
import logging
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer, RuleSerializer

logger = logging.getLogger("telescope")
logger.setLevel(logging.INFO)


@api_view(["POST"])
def import_company_data(request):
    """
    :param request:
    """
    if request.FILES.get("file"):
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded_file))
        company_data = list(reader)
    elif isinstance(request.data, list):
        company_data = request.data
    else:
        return Response(
            {"error": "Invalid data format. Provide a CSV file or a JSON array."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    imported_count = 0
    for row in company_data:
        for key, value in row.items():
            if value == "N/A":
                row[key] = None

        try:
            row["employee_locations"] = json.loads(
                row["employee_locations"].replace("'", '"')
            )
        except (json.JSONDecodeError, KeyError):
            row["employee_locations"] = None

        serializer = CompanySerializer(data=row)
        if serializer.is_valid():
            serializer.save()
            imported_count += 1
        else:
            print(f"Error importing row: {row} - {serializer.errors}")

    return Response(
        {"message": f"Successfully imported {imported_count} records."},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def get_companies(request):
    """
    :param request:
    """
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def process_company(request):
    """
    :param request:
    """
    data = request.data
    company_urls = data.get("companies", [])
    rules = data.get("rules", [])

    is_valid, validated_rules = validate_rules(rules)
    if not is_valid:
        return Response(
            {"error": "Invalid rules data. {validated_rules.errors}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if company_urls:
        companies = Company.objects.filter(url__in=company_urls)
    else:
        companies = Company.objects.all()

    processed_data = []
    for company in companies:

        feature_values = {}
        company = pre_process_hook(company)
        logger.info(f"Processing company: {company.company_name}")

        for rule in validated_rules:

            feature_value = get_feature_value(company, rule)
            if feature_value is None:
                logger.error(
                    f"Feature value not found for rule: {rule.input}, skipping"
                )
                continue

            matched = apply_operation(rule, company, feature_value)
            feature_values[rule.feature_name] = rule.match if matched else rule.default

        for rule.feature_name, value in feature_values.items():
            setattr(company, rule.feature_name, value)

        all_companies = Company.objects.all()
        similar_companies = get_similar_companies(company, all_companies)

        logger.info(f"Processed data: {feature_values}")
        serializer = CompanySerializer(company)
        company_data = serializer.data
        company_data.update(feature_values)

        # Similar companies based on the description and industry of
        # the processed companies
        company_data["similar_companies"] = similar_companies

        processed_data.append(company_data)

        logger.info(f"Processed data: {company_data}")

    return Response(processed_data, status=status.HTTP_200_OK)


def validate_rules(rules):
    """
    :param rules:
    """

    validated_rules = []
    for rule_data in rules:
        serializer = RuleSerializer(data=rule_data)
        if serializer.is_valid():
            rule = serializer.create(serializer.validated_data)
            validated_rules.append(rule)
        else:
            logger.error(f"Invalid rule data: {rule_data}, errors: {serializer.errors}")
            return False, serializer.errors

    logger.info(f"Validated rules: {validated_rules}")
    return True, validated_rules


def pre_process_hook(company):
    """
    :param company:
    """

    logger.info(f"Getting pre-processing values for company: {company.company_name}")
    current_year = timezone.now().year
    company_age = current_year - company.founded_year if company.founded_year else None

    is_usa_based = (
        company.headquarters_city is not None and "(USA)" in company.headquarters_city
    )

    company.company_age = company_age
    company.is_usa_based = is_usa_based
    company.is_saas = is_saas_company(company)
    company.last_processed = timezone.now()

    logger.info(
        f"Company age: {company.company_age}, USA based: {is_usa_based}, SaaS: {company.is_saas}"
    )
    company.save()
    return company


def get_feature_value(company, rule):
    """

    :param company:
    :param rule:

    """

    logger.info(f"Getting feature value for rule: {rule.input}")
    feature_value = None
    try:
        feature_value = getattr(company, rule.input)
    except AttributeError:
        logger.error(f"Error: Invalid feature name - {rule.input}")
        raise
    return feature_value


def apply_operation(rule, company, feature_value):
    """

    :param rule:
    :param company:
    :param feature_value:

    """

    logger.info(f"Applying rule: {rule.input} {rule.operation} {feature_value}")
    matched = False
    if (
        rule.input == "total_employees"
        and "greater_than" in rule.operation
        and feature_value is not None
    ):
        matched = feature_value > rule.operation["greater_than"]

    elif (
        rule.input == "company_age"
        and "less_than" in rule.operation
        and feature_value is not None
    ):
        matched = (
            feature_value < rule.operation["less_than"]
            if feature_value is not None
            else False
        )

    elif (
        rule.input == "is_usa_based"
        and "equal" in rule.operation
        and feature_value is not None
    ):
        matched = feature_value == rule.operation["equal"]
    elif (
        rule.input == "is_saas"
        and "equal" in rule.operation
        and feature_value is not None
    ):
        matched = company.is_saas == rule.operation["equal"]

    logger.info(f"Matched: {matched}")

    return matched


def is_saas_company(company):
    """
    Determines if a company is a SaaS company based on its description and industry.
    """
    logger.info(f"Checking if {company.company_name} is a SaaS company")
    saas_keywords = [
        "saas",
        "software as a service",
        "subscription",
        "cloud-based",
        "cloud based",
        "hosted solution",
        "on-demand software",
        "web-based application",
        "software platform",
        "software",
    ]

    text = f"{company.description} {company.industry}".lower()

    for keyword in saas_keywords:
        if keyword in text:
            logger.info(f"{company.company_name} is a SaaS company")
            return True
    logger.info(f"{company.company_name} is not a SaaS company")
    return False


def calculate_similarity(company1, company2):
    """
    Calculates the similarity between two companies based on their description and industry.
    """
    logger.info(
        f"Calculating similarity between {company1.company_name} and {company2.company_name}"
    )
    keywords1 = f"{company1.description} {company1.industry}".lower().split()
    keywords2 = f"{company2.description} {company2.industry}".lower().split()

    common_keywords = set(keywords1) & set(keywords2)
    logger.info(f"Common keywords: {common_keywords}")
    return len(common_keywords)


def get_similar_companies(company, companies, num_recommendations=3):
    """
    Finds the most similar companies for a given company.
    """
    logger.info(f"Finding similar companies for {company.company_name}")
    similarities = []
    for other_company in companies:
        if company == other_company:
            continue
        similarity = calculate_similarity(company, other_company)
        similarities.append((other_company, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    similar_companies = [
        other_company.company_name
        for other_company, _ in similarities[:num_recommendations]
    ]
    logger.info(f"Similar companies: {similar_companies}")
    return similar_companies
