from django.urls import path

from . import views

app_name = "reporting"

urlpatterns = [
	path('', views.monthly_index, name='monthly_index'),
	# Annual
	# Quarterly
	path('quarterly-reports', views.quarters_index, name="quarters_report"),
	path('quarterly-issuance', views.quarter_issuance_report, name="quarter_issuance_report"),
	path('distribution-quarterly', views.quarter_distribution_report, name='quarter_dist_report'),
	path('visits-quarterly', views.quarter_visits_report, name='quarter_visits_report'),
	path('dsitribution-by-quarter/<str:quarter>/<str:mwaka>/', views.download_qdistribution_excel, name='county_quarter_dist'),
	# Monthly
	path('monthly-report/<str:user_year>/<int:user_month>/', views.monthly_report, name='monthly_report'),
	path('overall-monthly-filter', views.monthly_report, name="monthly_overall_filter"),
	path('region-distribution', views.region_monthly_distribution, name='region_distribution'),
	path('monthly-distribution', views.month_dist_filter, name="month_dist_filter"),
	path('monthly-issuance', views.month_issuance_filter, name="month_issuance_filter"),
	path('monthly-visits', views.month_visits_filter, name="month_visits_filter"),
	path('county-facility-distribution/<str:county>/<int:mwezi>/<int:mwaka>/', views.county_facility_distribution, name='county_facility_dist'),
	path('export-visits/<int:mwaka>/<int:mwezi>/', views.export_monthly_county_visits, name="export_monthly_county_visits"),
	# Autocomplete
	path('autocomplete/all-subcounties/', views.subcounty_autocomplete, name="scounty_autocomplete"),
]