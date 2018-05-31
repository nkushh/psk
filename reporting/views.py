from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from distribution.models import Nets_distributed, Distribution_report, Warehouse, Stocking_history
from facilities.models import Counties, Epidemiological_zones, Facilities, Regions
from visits.models import Visit
import datetime, calendar


# Create your views here.
# Monthly reports module

# CURRENT MONTH AND YEAR
@login_required(login_url="login")
def monthly_index(request):
	today = datetime.datetime.now()
	mwaka = today.year
	last_month = today.month - 1

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	new_facilities = Facilities.objects.filter(date_added__year=mwaka, date_added__month=today.month).count()
	nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=today.month).aggregate(total_delivered=Sum('nets_issued'))
	nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=today.month).aggregate(total_issued=Sum('total_nets'))

	# Previous month and current year
	prev_month_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=last_month).aggregate(prev_delivered=Sum('nets_issued'))
	prev_month_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_issued=Sum('total_nets'))
	
	# Current month and year
	nets_to_anc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=today.month).aggregate(total_anc=Sum('anc_nets'))
	nets_to_cwc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=today.month).aggregate(total_cwc=Sum('cwc_nets'))
	
	# Previous month and current year
	prev_month_anc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_anc=Sum('anc_nets'))
	prev_month_cwc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_cwc=Sum('cwc_nets'))
	
	visits = Visit.objects.filter(date_recorded__year=mwaka, date_recorded__month=today.month).count()
	context = {
		'months_choices' : months_choices,
		'nets_delivered' : nets_delivered,
		'new_facilities' : new_facilities,
		'nets_issued' : nets_issued,
		'nets_to_anc' : nets_to_anc,
		'nets_to_cwc' : nets_to_anc,
		'prev_month_anc' : prev_month_anc,
		'prev_month_cwc' : prev_month_cwc,
		'prev_month_delivered' : prev_month_delivered,
		'prev_month_issued' : prev_month_issued,
		'visits' : visits
	}
	template = "reporting/monthly-index.html"
	return render(request, template, context)


# DYNAMIC MONTHLY REPORT
@login_required(login_url="login")
def monthly_report(request, user_year, user_month):
	today = datetime.datetime.now()
	mwaka = user_year
	last_month = user_month - 1

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	new_facilities = Facilities.objects.filter(date_added__year=mwaka, date_added__month=user_month).count()
	nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=user_month).aggregate(total_delivered=Sum('nets_issued'))
	nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=user_month).aggregate(total_issued=Sum('total_nets'))

	# Previous month and current year
	prev_month_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=last_month).aggregate(prev_delivered=Sum('nets_issued'))
	prev_month_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_issued=Sum('total_nets'))
	
	# Current month and year
	nets_to_anc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=user_month).aggregate(total_anc=Sum('anc_nets'))
	nets_to_cwc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=user_month).aggregate(total_cwc=Sum('cwc_nets'))
	
	# Previous month and current year
	prev_month_anc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_anc=Sum('anc_nets'))
	prev_month_cwc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_cwc=Sum('cwc_nets'))
	
	visits = Visit.objects.filter(date_recorded__year=mwaka, date_recorded__month=user_month).count()
	prev_month_visits = Visit.objects.filter(date_recorded__year=mwaka, date_recorded__month=last_month).count()

	context = {
		'months_choices' : months_choices,
		'nets_delivered' : nets_delivered,
		'new_facilities' : new_facilities,
		'nets_issued' : nets_issued,
		'nets_to_anc' : nets_to_anc,
		'nets_to_cwc' : nets_to_anc,
		'prev_month_anc' : prev_month_anc,
		'prev_month_cwc' : prev_month_cwc,
		'prev_month_delivered' : prev_month_delivered,
		'prev_month_issued' : prev_month_issued,
		'prev_month_visits' : prev_month_visits,
		'visits' : visits
	}
	template = "reporting/monthly-index.html"
	return render(request, template, context)


# Annual reports module

# CURRENT YEAR
@login_required(login_url="login")
def annual_index(request):
	today = datetime.datetime.now()
	mwaka = today.year
	last_year = mwaka - 1

	year_choices = []
	for i in range(2008,mwaka):
	    year_choices.append(i)

	new_facilities = Facilities.objects.filter(date_added__year=mwaka).count()
	nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka).aggregate(total_delivered=Sum('nets_issued'))
	nets_issued = Distribution_report.objects.filter(dist_year=mwaka).aggregate(total_issued=Sum('total_nets'))

	# Previous year
	prev_year_delivered = Nets_distributed.objects.filter(date_issued__year=last_year).aggregate(prev_delivered=Sum('nets_issued'))
	prev_year_issued = Distribution_report.objects.filter(dist_year=last_year).aggregate(prev_issued=Sum('total_nets'))
	
	# Current year
	nets_to_anc = Distribution_report.objects.filter(dist_year=mwaka).aggregate(total_anc=Sum('anc_nets'))
	nets_to_cwc = Distribution_report.objects.filter(dist_year=mwaka).aggregate(total_cwc=Sum('cwc_nets'))
	
	# Previous current year
	prev_year_anc = Distribution_report.objects.filter(dist_year=last_year).aggregate(prev_anc=Sum('anc_nets'))
	prev_year_cwc = Distribution_report.objects.filter(dist_year=last_year).aggregate(prev_cwc=Sum('cwc_nets'))
	
	visits = Visit.objects.filter(date_recorded__year=mwaka).count()
	context = {
		'year_choices' : year_choices,
		'nets_delivered' : nets_delivered,
		'new_facilities' : new_facilities,
		'nets_issued' : nets_issued,
		'nets_to_anc' : nets_to_anc,
		'nets_to_cwc' : nets_to_anc,
		'prev_year_anc' : prev_year_anc,
		'prev_year_cwc' : prev_year_cwc,
		'prev_year_delivered' : prev_year_delivered,
		'prev_year_issued' : prev_year_issued,
		'visits' : visits
	}
	template = "reporting/monthly-index.html"
	return render(request, template, context)


# DYNAMIC ANNUAL REPORT
@login_required(login_url="login")
def annual_report(request, user_year):
	today = datetime.datetime.now()
	mwaka = user_year
	prev_year = user_year - 1

	year_choices = []
	for i in range(2007,today.year):
	    year_choices.append(i)

	new_facilities = Facilities.objects.filter(date_added__year=mwaka).count()
	nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka).aggregate(total_delivered=Sum('nets_issued'))
	nets_issued = Distribution_report.objects.filter(dist_year=mwaka).aggregate(total_issued=Sum('total_nets'))

	# Previous year
	prev_year_delivered = Nets_distributed.objects.filter(date_issued__year=prev_year).aggregate(prev_delivered=Sum('nets_issued'))
	prev_year_issued = Distribution_report.objects.filter(dist_year=prev_year).aggregate(prev_issued=Sum('total_nets'))
	
	# Current year
	nets_to_anc = Distribution_report.objects.filter(dist_year=mwaka).aggregate(total_anc=Sum('anc_nets'))
	nets_to_cwc = Distribution_report.objects.filter(dist_year=mwaka).aggregate(total_cwc=Sum('cwc_nets'))
	
	# Previous current year
	prev_year_anc = Distribution_report.objects.filter(dist_year=prev_year).aggregate(prev_anc=Sum('anc_nets'))
	prev_year_cwc = Distribution_report.objects.filter(dist_year=prev_year).aggregate(prev_cwc=Sum('cwc_nets'))
	
	visits = Visit.objects.filter(date_recorded__year=mwaka).count()
	prev_month_visits = Visit.objects.filter(date_recorded__year=prev_year).count()

	context = {
		'year_choices' : year_choices,
		'nets_delivered' : nets_delivered,
		'new_facilities' : new_facilities,
		'nets_issued' : nets_issued,
		'nets_to_anc' : nets_to_anc,
		'nets_to_cwc' : nets_to_anc,
		'prev_year_anc' : prev_year_anc,
		'prev_year_cwc' : prev_year_cwc,
		'prev_year_delivered' : prev_year_delivered,
		'prev_year_issued' : prev_year_issued,
		'prev_year_visits' : prev_year_visits,
		'prev_year_visits' : prev_year_visits,
		'visits' : visits
	}
	template = "reporting/monthly-index.html"
	return render(request, template, context)



@login_required(login_url='login')
def region_monthly_distribution(request):
	today = datetime.datetime.now()
	mwaka = today.year
	mwezi = today.month

	current_month = Nets_distributed.objects.filter(date_issued__month=mwezi, date_issued__year=mwaka).values('facility__psk_region').annotate(total_nets=Sum('nets_issued')).order_by('-total_nets')
	current_year = Nets_distributed.objects.filter(date_issued__year=mwaka).values('facility__psk_region').annotate(total_nets=Sum('nets_issued')).order_by('-total_nets')

	template = "reporting/region-distribution.html"
	context = {
		'current_month' : current_month,
		'current_year' : current_year
	}

	return render(request, template, context)




