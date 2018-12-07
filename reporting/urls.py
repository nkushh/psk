from django.urls import path

from . import views

app_name = "reporting"

urlpatterns = [
	path('', views.monthly_index, name='monthly_index'),
	path('monthly-report/<str:user_year>/<int:user_month>/', views.monthly_report, name='monthly_report'),
	path('overall-monthly-filter', views.monthly_report, name="monthly_overall_filter"),
	path('quarterly-reports', views.quarters_index, name="quarters_report"),
	path('dsitribution-by-quarter/<str:quarter>/<str:mwaka>/', views.download_qdistribution_excel, name='county_quarter_dist'),
	path('region-distribution', views.region_monthly_distribution, name='region_distribution'),
	path('monthly-distribution', views.month_dist_filter, name="month_dist_filter"),
	path('monthly-issuance', views.month_issuance_filter, name="month_issuance_filter"),
]