from django.urls import path

from . import views

app_name = 'facilities'

urlpatterns = [
	# Facilities
	path('', views.dashboard, name="dashboard"),
	path('facilities/', views.facilities, name="facilities"),
	path('county-facilities/<str:county_name>/', views.county_facilities, name="county_facilities"),
	path('subcounty-facilities/<str:county_name>/<str:subcounty>/', views.subcounty_facilities, name="subcounty_facilities"),
	path('add-facility', views.new_facility, name="new_facility"),
	path('new-facilities', views.facilities_excel_upload, name="new_facilities"),
	path('change-county-name', views.county_name_change, name="county_name_change"),
	path('facility-detail/<int:facility_pk>/', views.facility_details, name="facility_details"),
	# Autocomplete
	path('autocomplete/all-facilities/', views.facilities_autocomplete, name="autocomplete"),
	path('search', views.facility_search, name='search_facility'),
	path('download-facilities', views.download_facilities_excel, name="excel_facilities_download"),
	path('update-facility/<int:facility_pk>/', views.update_facility, name="update_facility"),
	path('delete-facilities', views.delete_all_facilities, name="delete_facilities"),
	path('delete-facility/<int:facility_pk>/', views.delete_facility, name="delete_facility"),
	# Regions
	path('psk-regions', views.psk_regions, name="psk_regions"),
	path('new-region', views.new_region, name="new_region"),
	path('update-region/<int:region_pk>/', views.update_region, name="update_region"),
	path('delete-region/<int:region_pk>/', views.delete_region, name="delete_region"),
	# Zones
	path('psk-zones', views.transmission_zones, name="transmission_zones"),
	path('new-zone', views.new_zone, name="new_zone"),
	path('update-zone/<int:zone_pk>/', views.update_zone, name="update_zone"),
	path('delete-zone/<int:zone_pk>/', views.delete_zone, name="delete_zone"),
	# Settings
	path('facility-settings', views.facility_settings, name="facility_settings"),
	path('set-facilities-region/<str:psk_region>/', views.set_facility_region, name="set_facility_region"),
	path('set-facilities-zone/<str:psk_zone>/', views.set_facility_zone, name="set_facility_zone"),
	path('change-region-name', views.region_name_change, name="region_name_change"),
]