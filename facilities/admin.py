from django.contrib import admin
from .models import Counties, Facilities

# Register your models here.
class FacilityAdmin(admin.ModelAdmin):
	search_fields = ('facility_name', 'mfl_code')

admin.site.register(Counties)
admin.site.register(Facilities,FacilityAdmin)