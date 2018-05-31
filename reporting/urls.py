from django.urls import path

from . import views

app_name = "reporting"

urlpatterns = [
	path('', views.monthly_index, name='monthly_index'),
	path('monthly-report/<str:user_year>/<int:user_month>/', views.monthly_report, name='monthly_report'),
	path('region-distribution', views.region_monthly_distribution, name='region_distribution'),
]