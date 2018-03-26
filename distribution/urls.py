from django.urls import path

from . import views

app_name = 'distribution'

urlpatterns = [
	path('nets-distribution', views.distribution_index, name='nets_distribution'),
	path('nets-issuance', views.record_nets_issued, name='issue_nets' ),
	path('nets-to-facilities', views.nets_issued_to_facilities, name='nets_to_facilities' ),
	path('record-distribution', views.record_distribution, name="record_distribution"),
	path('nets-distributed', views.nets_distributed, name='nets_distributed'),
]