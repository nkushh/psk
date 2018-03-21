from django.db import models

# Create your models here.
class Regions(models.Model):
	region_name = models.CharField(max_length=200)
	date_created  = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.region_name

class Facility_types(models.Model):
	type_name = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.type_name

class Facility_ownership(models.Model):
	ownership_name = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.ownership_name

class Epidemiological_zones(models.Model):
	zone_name = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.zone_name

class Facilities(models.Model):
	# psk_region = models.CharField(max_length=200)
	mfl_code = models.CharField(max_length=200)
	facility_name = models.CharField(max_length=200)
	county = models.CharField(max_length=200)
	sub_county = models.CharField(max_length=200)
	# facility_type = models.CharField(max_length=200, default="")
	facility_ownership = models.CharField(max_length=200, default="")
	epidemiological_zone = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1)

	def __str__(self):
		return self.facility_name

class Profile(models.Model):
	name = models.CharField(max_length=200)
	sex = models.CharField(max_length=200)
	age = models.CharField(max_length=200)

	def __str__(self):
		return self.name


