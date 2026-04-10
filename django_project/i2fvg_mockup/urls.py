from django.urls import path

from i2fvg_mockup import views


app_name = "i2fvg_mockup"

urlpatterns = [
    path("", views.home, name="home"),
    path("companies/", views.company_list, name="company_list"),
    path("financial/", views.financial_dashboard, name="financial_dashboard"),
    path("eu-projects/", views.project_list, name="eu_projects_dashboard"),
    path("companies/connected/", views.connected_company_list, name="connected_company_list"),
    path("companies/<str:cf>/", views.company_detail, name="company_detail"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/<str:project_id>/", views.project_detail, name="project_detail"),
]
