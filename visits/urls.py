from django.urls import path

from . import views

app_name = "visits"

urlpatterns = [
	path('visits', views.visits_index, name="visits_index"),
	path('coordinator-visits/<int:coordinator_pk>/', views.coordinator_visits, name="coordinator_visits"),
	path('coordinator_aggregate-visits', views.coordinators_aggregate_visits, name="coordinators_aggregate_visits"),
	path('record-visit', views.record_visit, name="record_visit"),
	path('email-sender', views.email_sender, name="send_mail"),
]