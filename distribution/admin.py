from django.contrib import admin
from .models import Nets_distributed, Distribution_report, Distribution_target, Warehouse

# Register your models here.
admin.site.register(Nets_distributed)
admin.site.register(Distribution_report)
admin.site.register(Distribution_target)
admin.site.register(Warehouse)
