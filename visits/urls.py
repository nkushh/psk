from django.urls import path

from . import views

app_name = "visits"

urlpatterns = [
	path('visits', views.visits_index, name="visits_index"),
	path('record-visit', views.record_visit, name="record_visit"),
	path('forms', views.visit_form, name="visit_form"),
]