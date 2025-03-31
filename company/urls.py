from django.urls import path
from . import views

urlpatterns = [
    path("import_company_data/", views.import_company_data, name="import_company_data"),
    path("get_companies/", views.get_companies, name="get_companies"),
    path("process_company/", views.process_company, name="process_company"),
]
