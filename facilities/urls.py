from django.urls import path

from . import views

app_name = 'facilities'

urlpatterns = [
	path('', views.dashboard, name="dashboard"),
	path('facilities', views.facilities, name="facilities"),
	path('add-facility', views.new_facility, name="add_facility"),
	path('new-facilities', views.excel_upload, name="new_facilities"),
	path('facility-detail/<int:facility_pk>/', views.facility_details, name="facility_details"),
	path('autocomplete/all-facilities/', views.facilities_autocomplete, name="autocomplete"),
	path('search', views.facility_search, name='search_facility'),
]