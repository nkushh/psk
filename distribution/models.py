import datetime, calendar
from django.db import models
from facilities.models import Counties, Facilities

# Create your models here.
class Warehouse(models.Model):
	warehouse_name = models.CharField(max_length=200)
	county = models.ForeignKey(Counties, on_delete=models.CASCADE)
	location = models.CharField(max_length=200)
	contact_person = models.CharField(max_length=200)
	contact = models.CharField(max_length=200)
	stock_balance = models.IntegerField(default=0)
	date_added = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.warehouse_name


class Stocking_history(models.Model):
	warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
	donor = models.CharField(max_length=200)
	nets_quantity = models.IntegerField(default=0)
	date_stocked = models.DateField()

	def __str__(self):
		return self.warehouse.warehouse_name


class Nets_distributed(models.Model):
	facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
	invoice_no = models.CharField(max_length=200, default="")
	warehouse = models.CharField(max_length=255, default="")
	nets_issued = models.IntegerField()
	donor_code = models.CharField(max_length=20, default="")
	date_issued = models.DateField()
	date_recorded = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.facility.facility_name

class Distribution_report(models.Model):
	facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
	dist_month = models.IntegerField()
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

# class Nets_return(models.Model):
# 	facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
# 	nets_returned = models.IntegerField()
# 	date_returned = models.DateField()
# 	date_recorded = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.facility.facility_name


