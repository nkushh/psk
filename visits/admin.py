from django.contrib import admin
from .models import Visit

# Register your models here.
class VisitsAdmin(admin.ModelAdmin):
	list_display = ['facility', 'supervisor', 'visit_date']
	list_filter = ['visit_date', 'date_recorded']
	search_fields = ['visit_date']

	class Meta:
		model = Visit

admin.site.register(Visit, VisitsAdmin)
