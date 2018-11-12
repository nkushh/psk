from distribution.models import Nets_distributed, Distribution_report, Warehouse, Stocking_history
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render
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
	counties = Facilities.objects.values('county').distinct()
	miaka = range(2010,mwaka+1)

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
		'counties' : counties,
		'months_choices' : months_choices,
		'miaka' : miaka,
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
	counties = Facilities.objects.values('county').distinct()

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
		'counties' : counties,
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

def quarters_index(request):
	today = datetime.datetime.now()
	mwaka = today.year
	# Quarter one
	q1_distribution = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).aggregate(q1_deliverd = Sum('nets_issued'))
	q1_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=1, dist_year__lte=mwaka, dist_month__lte=3).aggregate(q1_issued = Sum('total_nets'))
	q1_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=1, visit_date__year__lte=mwaka, visit_date__month__lte=3).count()
	# Quarter two
	q2_distribution = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).aggregate(q2_deliverd = Sum('nets_issued'))
	q2_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=4, dist_year__lte=mwaka, dist_month__lte=6).aggregate(q2_issued = Sum('total_nets'))
	q2_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=4, visit_date__year__lte=mwaka, visit_date__month__lte=6).count()
	# Quarter three
	q3_distribution = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).aggregate(q3_deliverd = Sum('nets_issued'))
	q3_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=7, dist_year__lte=mwaka, dist_month__lte=9).aggregate(q3_issued = Sum('total_nets'))
	q3_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=7, visit_date__year__lte=mwaka, visit_date__month__lte=9).count()
	# Quarter four
	q4_distribution = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).aggregate(q4_deliverd = Sum('nets_issued'))
	q4_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=10, dist_year__lte=mwaka, dist_month__lte=12).aggregate(q4_issued = Sum('total_nets'))
	q4_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=10, visit_date__year__lte=mwaka, visit_date__month__lte=12).count()
	counties = Facilities.objects.values('county').distinct()
	
	template = "reporting/quarter-index.html"
	context = {
		'counties' : counties,
		'q1_distribution' : q1_distribution,
		'q1_issuance' : q1_issuance,
		'q1_visits' : q1_visits,
		'q2_distribution' : q2_distribution,
		'q2_issuance' : q2_issuance,
		'q2_visits' : q2_visits,
		'q3_distribution' : q3_distribution,
		'q3_issuance' : q3_issuance,
		'q3_visits' : q3_visits,
		'q4_distribution' : q4_distribution,
		'q4_issuance' : q4_issuance,
		'q4_visits' : q4_visits
	}

	return render(request, template, context)

@login_required(login_url='login')
def get_quarter_report(request, quarter, mwaka):
	today = datetime.datetime.now()
	current_year = today.year

	# records = Distribution_report.objects.values('facility__county').annotate(Sum('total_nets')).distinct()
	if quarter == "first":
		q_report = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=1, visit_date__year__lte=mwaka, visit_date__month__lte=3)
	elif quarter == "second":
		q_report = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=4, visit_date__year__lte=mwaka, visit_date__month__lte=6)
	elif quarter == "third":
		q_report = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=7, visit_date__year__lte=mwaka, visit_date__month__lte=9)
	elif quarter == "fourth":
		q_report = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=10, visit_date__year__lte=mwaka, visit_date__month__lte=12)
	else:
		q_report = Visit.objects.filter(visit_date__year__gte=current_year)

	template = "distribution/counties-issuance.html"
	context = {
		'q_report' : q_report
	}
	return render(request, template, context)



def download_qdistribution_excel(request, quarter, mwaka):
	today = datetime.datetime.now()
	if not mwaka:
		mwaka = today.year
	else:
		mwaka = mwaka
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="distribution.csv"'

	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])

	if quarter == "first":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "second":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "third":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "fourth":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	else:
		quarter_dist = Nets_distributed.objects.filter(date_issued__year=mwaka).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	
	for report in quarter_dist:
	    writer.writerow(report)

	return response

