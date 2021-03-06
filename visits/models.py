from django.db import models
from django.contrib.auth.models import User
from datetime import date

from facilities.models import Facilities
# Create your models here.
class Visit(models.Model):
	supervisor = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	facility = models.ForeignKey(Facilities, on_delete=models.CASCADE)
	visit_date = models.DateField(default=date.today)
	reporting_frequency = models.IntegerField(default=0)
	quarter_order = models.IntegerField(default=0)
	challenge_solver = models.CharField(max_length=200, default="N/A")
	ojt_perfomed = models.IntegerField(default=0)
	policy_compliance = models.IntegerField(default=0)
	non_compliance_reason = models.TextField(default="N/A")
	new_anc_moh711 = models.IntegerField(default=0)
	nets_anc_moh711 = models.IntegerField(default=0)
	nets_anc_fnprc = models.IntegerField(default=0)
	nets_anc_variance = models.IntegerField(default=0)
	new_cwc_moh710 = models.IntegerField(default=0)
	nets_cwc_moh711 = models.IntegerField(default=0)
	nets_cwc_fnprc = models.IntegerField(default=0)
	nets_cwc_variance = models.IntegerField(default=0)
	book_bal = models.IntegerField(default=0)
	physical_count = models.IntegerField(default=0)
	balance_variance = models.IntegerField(default=0)
	bal_variance_reason = models.TextField(default="N/A")
	ld_quantity = models.IntegerField(null=True, default=0)
	ld_invoice_no = models.CharField(max_length=200, null=True)
	ld_date = models.DateField(default=date.today, null=True, )
	lld_quantity = models.IntegerField(default=0, blank=True, null=True, )
	lld_invoice_no = models.CharField(max_length=200, blank=True, null=True, )
	lld_date = models.DateField(default=date.today, blank=True, null=True, )
	amc = models.FloatField(default=0)
	months_of_stock = models.FloatField(default=0)
	confirmable_cwc = models.CharField(max_length=200)
	confirmable_anc = models.CharField(max_length=200)
	store_type = models.CharField(max_length=200)
	stock_control_card = models.IntegerField(default=0)
	store_access = models.CharField(max_length=200, default="")
	pests_risk = models.CharField(max_length=200, default="")
	fire_prevention = models.IntegerField(default=0)
	fire_prevention_mechanism = models.CharField(max_length=200)
	other_remarks = models.TextField(null=True)
	date_recorded = models.DateTimeField(auto_now_add=True)
	risk_level = models.CharField(max_length=10, default="Low")
	status = models.IntegerField(default=0)

	def __str__(self):
		return self.facility.facility_name
