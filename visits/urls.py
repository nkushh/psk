from django.urls import path

from . import views

app_name = "visits"

urlpatterns = [
	path('visits', views.visits_index, name="visits_index"),
	path('list_visits', views.list_view, name="list_view"),
	path('visit-details/<int:visit_id>/', views.visit_details, name="visit_details"),
	path('coordinator-visits/<int:coordinator_pk>/', views.coordinator_visits, name="coordinator_visits"),
	path('coordinator_aggregate-visits', views.coordinators_aggregate_visits, name="coordinators_aggregate_visits"),
	path('monthly-cordinator-aggregate/<int:mwezi>/', views.monthly_coordinators_aggregate_visits, name="monthly_coordinators_aggregate_visits"),
	path('monthly-visits/<int:mwezi>/', views.month_visits, name="month_visits"),
	path('record-visit', views.record_visit, name="record_visit"),
	path('email-sender', views.email_sender, name="send_mail"),
	path('set-amc', views.set_amc, name="set_amc"),
	path('update-risk-level', views.update_risk_level, name="update_risk_level")
]