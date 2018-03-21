import datetime, calendar
from django.db import models
from facilities.models import Facilities

# Create your models here.
class Nets_distributed(models.Model):
	facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
	invoice_no = models.CharField(max_length=200, default="")
	nets_issued = models.IntegerField()
	date_issued = models.DateField()
	date_recorded = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.facility.facility_name

class Distribution_report(models.Model):
	facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
	dist_month = models.CharField(max_length=20)
	dist_year = models.CharField(max_length=5)
	bal_bf = models.IntegerField(default=0)
	cwc_nets = models.IntegerField(default=0)
	anc_nets = models.IntegerField(default=0)
	others_nets = models.IntegerField(default=0)
	total_nets = models.IntegerField(default=0)
	bal_cf = models.IntegerField(default=0)
	date_recorded = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.facility.facility_name


