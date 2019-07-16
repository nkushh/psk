from distribution.models import Nets_distributed, Distribution_report, Warehouse, Stocking_history
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from facilities.models import Counties, Epidemiological_zones, Facilities, Regions
from visits.models import Visit
import datetime, calendar, csv



# Create your views here.
# Monthly reports module

# CURRENT MONTH AND YEAR
@login_required(login_url="login")
def monthly_index(request):
	today = datetime.datetime.now()
	mwaka = today.year
	last_year = mwaka - 1

	if today.month == 1:
		last_month = 12
		# Previous month and current year
		prev_month_delivered = Nets_distributed.objects.filter(date_issued__year=last_year, date_issued__month=last_month).aggregate(prev_delivered=Sum('nets_issued'))
		prev_month_issued = Distribution_report.objects.filter(dist_year=last_year, dist_month=last_month).aggregate(prev_issued=Sum('total_nets'))
		# Current month and year
		nets_to_anc = Distribution_report.objects.filter(dist_year=last_year, dist_month=today.month).aggregate(total_anc=Sum('anc_nets'))
		nets_to_cwc = Distribution_report.objects.filter(dist_year=last_year, dist_month=today.month).aggregate(total_cwc=Sum('cwc_nets'))

		# Previous month and current year
		prev_month_anc = Distribution_report.objects.filter(dist_year=last_year, dist_month=last_month).aggregate(prev_anc=Sum('anc_nets'))
		prev_month_cwc = Distribution_report.objects.filter(dist_year=last_year, dist_month=last_month).aggregate(prev_cwc=Sum('cwc_nets'))

		# Previous month visits
		prev_month_visits = Visit.objects.filter(date_recorded__year=last_year, date_recorded__month=last_month).count()
	else:
		last_month = today.month - 1
		# Previous month and current year
		prev_month_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=last_month).aggregate(prev_delivered=Sum('nets_issued'))
		prev_month_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_issued=Sum('total_nets'))
		# Current month and year
		nets_to_anc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=today.month).aggregate(total_anc=Sum('anc_nets'))
		nets_to_cwc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=today.month).aggregate(total_cwc=Sum('cwc_nets'))

		# Previous month and current year
		prev_month_anc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_anc=Sum('anc_nets'))
		prev_month_cwc = Distribution_report.objects.filter(dist_year=mwaka, dist_month=last_month).aggregate(prev_cwc=Sum('cwc_nets'))

		# Previous month visits
		prev_month_visits = Visit.objects.filter(date_recorded__year=mwaka, date_recorded__month=last_month).count()

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	prev_month = calendar.month_abbr[last_month]
	current_month = calendar.month_abbr[today.month]

	new_facilities = Facilities.objects.filter(date_added__year=mwaka, date_added__month=today.month).count()
	nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=today.month).aggregate(total_delivered=Sum('nets_issued'))
	nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=today.month).aggregate(total_issued=Sum('total_nets'))
	counties = Counties.objects.all().order_by('county_name')
	visits = Visit.objects.filter(date_recorded__year=mwaka, date_recorded__month=today.month).count()
	miaka = range(2018,mwaka+1)

	sub_counties = Facilities.objects.values('sub_county').distinct()
	context = {
		'counties' : counties,
		'current_month' : current_month,
		'months_choices' : months_choices,
		'miaka' : miaka,
		'nets_delivered' : nets_delivered,
		'new_facilities' : new_facilities,
		'nets_issued' : nets_issued,
		'nets_to_anc' : nets_to_anc,
		'nets_to_cwc' : nets_to_anc,
		'prev_month' : prev_month,
		'prev_month_anc' : prev_month_anc,
		'prev_month_cwc' : prev_month_cwc,
		'prev_month_delivered' : prev_month_delivered,
		'prev_month_issued' : prev_month_issued,
		'prev_month_visits' : prev_month_visits,
		'sub_counties' : sub_counties,
		'visits' : visits
	}
	template = "reporting/monthly-index.html"
	return render(request, template, context)


# DYNAMIC MONTHLY REPORT
@login_required(login_url="login")
def monthly_report(request):
	today = datetime.datetime.now()
	mwaka = today.year
	mwezi = today.month


	if request.method == "POST":
		user_year = request.POST['mwaka']
		user_month = request.POST['mwezi']
		last_month = int(user_month) - 1
	else:
		user_year = mwaka
		user_month = mwezi
		last_month = mwezi - 1


	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	new_facilities = Facilities.objects.filter(date_added__year=user_year, date_added__month=user_month).count()
	nets_delivered = Nets_distributed.objects.filter(date_issued__year=user_year, date_issued__month=user_month).aggregate(total_delivered=Sum('nets_issued'))
	nets_issued = Distribution_report.objects.filter(dist_year=user_year, dist_month=user_month).aggregate(total_issued=Sum('total_nets'))
	counties = Counties.objects.all().order_by('county_name')

	# Previous month and current year
	prev_month_delivered = Nets_distributed.objects.filter(date_issued__year=user_year, date_issued__month=last_month).aggregate(prev_delivered=Sum('nets_issued'))
	prev_month_issued = Distribution_report.objects.filter(dist_year=user_year, dist_month=last_month).aggregate(prev_issued=Sum('total_nets'))

	# Current month and year
	nets_to_anc = Distribution_report.objects.filter(dist_year=user_year, dist_month=user_month).aggregate(total_anc=Sum('anc_nets'))
	nets_to_cwc = Distribution_report.objects.filter(dist_year=user_year, dist_month=user_month).aggregate(total_cwc=Sum('cwc_nets'))

	# Previous month and current year
	prev_month_anc = Distribution_report.objects.filter(dist_year=user_year, dist_month=last_month).aggregate(prev_anc=Sum('anc_nets'))
	prev_month_cwc = Distribution_report.objects.filter(dist_year=user_year, dist_month=last_month).aggregate(prev_cwc=Sum('cwc_nets'))

	visits = Visit.objects.filter(date_recorded__year=user_year, date_recorded__month=user_month).count()
	prev_month_visits = Visit.objects.filter(date_recorded__year=user_year, date_recorded__month=last_month).count()

	miaka = range(2018,mwaka+1)
	current_month = calendar.month_abbr[int(user_month)]
	prev_month = calendar.month_abbr[int(last_month)]

	context = {
		'counties' : counties,
		'current_month' : current_month,
		'months_choices' : months_choices,
		'miaka' : miaka,
		'nets_delivered' : nets_delivered,
		'new_facilities' : new_facilities,
		'nets_issued' : nets_issued,
		'nets_to_anc' : nets_to_anc,
		'nets_to_cwc' : nets_to_anc,
		'prev_month' : prev_month,
		'prev_month_anc' : prev_month_anc,
		'prev_month_cwc' : prev_month_cwc,
		'prev_month_delivered' : prev_month_delivered,
		'prev_month_issued' : prev_month_issued,
		'prev_month_visits' : prev_month_visits,
		'visits' : visits,
		'mwaka' : user_year
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

@login_required(login_url='login')
def quarters_index(request):
	today = datetime.datetime.now()
	mwaka = today.year
	miaka = range(2018,mwaka+1)
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
	counties = Counties.objects.all().order_by('county_name')

	template = "reporting/quarter-index.html"
	context = {
		'counties' : counties,
		'miaka' : miaka,
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
	miaka = range(2018, current_year+1)

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
		'miaka' : miaka,
		'q_report' : q_report
	}
	return render(request, template, context)

# Quarterly nets distribution for all counties
@login_required(login_url='login')
def quarter_distribution_facilities_csv(request, quarter, mwaka):
	if quarter == "One":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).values_list('facility__facility_name','facility__county','nets_issued')
	elif quarter == "Two":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).values_list('facility__facility_name','facility__county','nets_issued')
	elif quarter == "Three":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).values_list('facility__facility_name','facility__county','nets_issued')
	elif quarter == "Four":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).values_list('facility__facility_name','facility__county','nets_issued')

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="quarterly_distribution.csv"'
	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])

	for report in quarter_dist:
		print(report)
		writer.writerow(report)

	return response



# Quarterly nets distribution for all counties CSV export
@login_required(login_url='login')
def quarter_distribution_csv(request, quarter, mwaka):
	if quarter == "One":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Two":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Three":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Four":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="quarterly_distribution.csv"'
	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])

	for report in quarter_dist:
		print(report)
		writer.writerow(report)

	return response

@login_required(login_url='login')
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

	if quarter == "First":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Second":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Third":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Fourth":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	else:
		quarter_dist = Nets_distributed.objects.filter(date_issued__year=mwaka).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')

	for report in quarter_dist:
	    writer.writerow(report)

	return response

# Monthly reporting filters
#
#
#
@login_required(login_url='login')
def month_dist_filter(request):
	if request.method=="POST":
		mwezi = request.POST['mwezi']
		mwaka = request.POST['mwaka']
		county = request.POST.get('county', False)

		template = "reporting/month_dist.html"
		if county:
			county = get_object_or_404(Counties, pk=county)
			distribution = Nets_distributed.objects.filter(date_issued__month=mwezi, date_issued__year=mwaka, facility__county=county.name).values('facility__facility_name').annotate(total_dist=Sum('nets_issued')).order_by('-total_dist')
			total_nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi, facility__county=county).aggregate(total_nets=Sum('nets_issued'))
			template = "reporting/county_month_dist.html"
		else:
			distribution =  Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).values('facility__county').annotate(total_dist=Sum('nets_issued')).order_by('-total_dist')
			total_nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).aggregate(total_nets=Sum('nets_issued'))
			# for record in distribution:
			# 	record['facility__countyy'] = get_object_or_404(Counties, pk=record['facility__countyy'])


		counties = Counties.objects.order_by('county_name')
		regions = Regions.objects.order_by('region_name')
		query_month = calendar.month_name[int(mwezi)]


		page = request.GET.get('page', 1)

		paginator = Paginator(distribution, 50)

		try:
			distribution = paginator.page(page)
		except PageNotAnInteger:
			distribution = paginator.page(1)
		except EmptyPage:
			distribution = paginator.page(paginator.num_pages)

		index = distribution.number - 1
		max_index = len(paginator.page_range)
		start_index = index - 5 if index >= 5 else 0
		end_index = index + 5 if index <= max_index - 5 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context = {
			'counties' : counties,
			'county' : county,
			'distribution' : distribution,
			'mwaka' : mwaka,
			'mwezi' : mwezi,
			'query_month' : query_month,
			'regions' : regions,
			'total_nets_delivered' : total_nets_delivered
		}

	return render(request, template, context)

@login_required(login_url='login')
def month_issuance_filter(request):
	if request.method=="POST":
		mwezi = request.POST['mwezi']
		mwaka = request.POST['mwaka']
		county = request.POST.get('county', False)
		template = "reporting/month_issuance.html"
		if county:
			county = get_object_or_404(Counties, pk=county)
			distribution = Distribution_report.objects.filter(dist_month=mwezi, dist_year=mwaka, facility__countyy=county).values('facility__facility_name').annotate(total_dist=Sum('total_nets')).order_by('-total_dist')
			total_nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi, facility__county=county).aggregate(total_nets=Sum('total_nets'))
			template = "reporting/county_month_issuance.html"
		else:
			distribution =  Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).values('facility__countyy').annotate(total_dist=Sum('total_nets')).order_by('-total_dist')
			total_nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).aggregate(total_nets=Sum('total_nets'))


		counties = Counties.objects.order_by('county_name')
		regions = Regions.objects.order_by('region_name')
		query_month = calendar.month_name[int(mwezi)]


		page = request.GET.get('page', 1)

		paginator = Paginator(distribution, 50)

		try:
			distribution = paginator.page(page)
		except PageNotAnInteger:
			distribution = paginator.page(1)
		except EmptyPage:
			distribution = paginator.page(paginator.num_pages)

		index = distribution.number - 1
		max_index = len(paginator.page_range)
		start_index = index - 5 if index >= 5 else 0
		end_index = index + 5 if index <= max_index - 5 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context = {
			'counties' : counties,
			'county' : county,
			'distribution' : distribution,
			'mwaka' : mwaka,
			'mwezi' : mwezi,
			'query_month' : query_month,
			'regions' : regions,
			'total_nets_issued' : total_nets_issued
		}

	return render(request, template, context)

@login_required(login_url='login')
def month_visits_filter(request):
	if request.method == "POST":
		mwaka = request.POST['mwaka']
		mwezi = request.POST['mwezi']
		county = request.POST.get('county', False)
		template = 'reporting/month_visits.html'
		if county:
			county = get_object_or_404(Counties, pk=county)
			visits = Visit.objects.filter(visit_date__year=mwaka, visit_date__month=mwezi, facility__countyy=county).values('facility__facility_name').annotate(total_visits=Count('id'))
			visits_sum = Visit.objects.filter(visit_date__year=mwaka, visit_date__month=mwezi, facility__county=county).count()
			template = 'reporting/county_month_visits.html'
		else:
			visits = Visit.objects.filter(visit_date__year=mwaka, visit_date__month=mwezi).values_list('facility__countyy').annotate(totalvisits=Count('id')).order_by('-totalvisits')
			visits_sum = Visit.objects.filter(visit_date__year=mwaka, visit_date__month=mwezi).count()

		counties = Counties.objects.order_by('county_name')
		regions = Regions.objects.order_by('region_name')
		query_month = calendar.month_name[int(mwezi)]


		page = request.GET.get('page', 1)

		paginator = Paginator(visits, 50)

		try:
			visits = paginator.page(page)
		except PageNotAnInteger:
			visits = paginator.page(1)
		except EmptyPage:
			visits = paginator.page(paginator.num_pages)

		index = visits.number - 1
		max_index = len(paginator.page_range)
		start_index = index - 5 if index >= 5 else 0
		end_index = index + 5 if index <= max_index - 5 else max_index
		page_range = paginator.page_range[start_index:end_index]

		context = {
			'counties' : counties,
			'county' : county,
			'mwaka' : mwaka,
			'mwezi' : mwezi,
			'query_month' : query_month,
			'regions' : regions,
			'visits' : visits,
			'visits_sum' : visits_sum
		}

	return render(request, template, context)


# Quarter reporting filters
# Quarterly nets distribution for all counties
@login_required(login_url='login')
def quarter_distribution_report(request):
	today = datetime.datetime.now()
	miaka = range(2018, today.year+1)

	if request.method == "POST":
		quarter = request.POST['quarter']
		mwaka = request.POST['mwaka']

		if quarter == "One":
			quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).values('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
			quarter_dist_total = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).aggregate(total_nets=Sum('nets_issued'))
		elif quarter == "Two":
			quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).values('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
			quarter_dist_total = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).aggregate(total_nets=Sum('nets_issued'))
		elif quarter == "Three":
			quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).values('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
			quarter_dist_total = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).aggregate(total_nets=Sum('nets_issued'))
		elif quarter == "Four":
			quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).values('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
			quarter_dist_total = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).aggregate(total_nets=Sum('nets_issued'))

		# for record in quarter_dist:
		# 	record['facility__countyy'] = get_object_or_404(Counties, pk=record['facility__countyy'])
		context = {
			'miaka' : miaka,
			'mwaka' : mwaka,
			'quarter' : quarter,
			'quarter_dist' : quarter_dist,
			'quarter_dist_total' : quarter_dist_total
		}
		template = "reporting/quarter-distribution.html"

	return render(request, template, context)


# Quarterly nets issuance for all counties
@login_required(login_url='login')
def quarter_issuance_report(request):
	today = datetime.datetime.now()
	miaka = range(2018, today.year+1)

	if request.method == "POST":
		quarter = request.POST['quarter']
		mwaka = request.POST['mwaka']

		if quarter == "One":
			quarter_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=1, dist_year__lte=mwaka, dist_month__lte=3).values_list('facility__countyy').annotate(totalnets=Sum('total_nets')).order_by('-totalnets')
			quarter_issuance_total = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=1, dist_year__lte=mwaka, dist_month__lte=3).aggregate(total_nets=Sum('total_nets'))
		elif quarter == "Two":
			quarter_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=4, dist_year__lte=mwaka, dist_month__lte=6).values_list('facility__countyy').annotate(totalnets=Sum('total_nets')).order_by('-totalnets')
			quarter_issuance_total = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=4, dist_year__lte=mwaka, dist_month__lte=6).aggregate(total_nets=Sum('total_nets'))
		elif quarter == "Three":
			quarter_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=7, dist_year__lte=mwaka, dist_month__lte=9).values_list('facility__countyy').annotate(totalnets=Sum('total_nets')).order_by('-totalnets')
			quarter_issuance_total = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=7, dist_year__lte=mwaka, dist_month__lte=9).aggregate(total_nets=Sum('total_nets'))
		elif quarter == "Four":
			quarter_issuance = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=10, dist_year__lte=mwaka, dist_month__lte=12).values_list('facility__countyy').annotate(totalnets=Sum('total_nets')).order_by('-totalnets')
			quarter_issuance_total = Distribution_report.objects.filter(dist_year__gte=mwaka, dist_month__gte=10, dist_year__lte=mwaka, dist_month__lte=12).aggregate(total_nets=Sum('total_nets'))

		context = {
			'miaka' : miaka,
			'mwaka' : mwaka,
			'quarter' : quarter,
			'quarter_issuance' : quarter_issuance,
			'quarter_issuance_total' : quarter_issuance_total
		}
		template = "reporting/quarter-issuance.html"

	return render(request, template, context)


# Quarterly nets issuance for all counties
@login_required(login_url='login')
def quarter_visits_report(request):
	today = datetime.datetime.now()
	miaka = range(2018, today.year+1)

	if request.method == "POST":
		quarter = request.POST['quarter']
		mwaka = request.POST['mwaka']

		if quarter == "One":
			quarter_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=1, visit_date__year__lte=mwaka, visit_date__month__lte=3).values_list('facility__countyy').annotate(totalvisits=Count('id')).order_by('-totalvisits')
			quarter_visits_total = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=1, visit_date__year__lte=mwaka, visit_date__month__lte=3).count()
		elif quarter == "Two":
			quarter_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=4, visit_date__year__lte=mwaka, visit_date__month__lte=6).values_list('facility__countyy').annotate(totalvisits=Count('id')).order_by('-totalvisits')
			quarter_visits_total = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=4, visit_date__year__lte=mwaka, visit_date__month__lte=6).count()
		elif quarter == "Three":
			quarter_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=7, visit_date__year__lte=mwaka, visit_date__month__lte=9).values_list('facility__countyy').annotate(totalvisits=Count('id')).order_by('-totalvisits')
			quarter_visits_total = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=7, visit_date__year__lte=mwaka, visit_date__month__lte=9).count()
		elif quarter == "Four":
			quarter_visits = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=10, visit_date__year__lte=mwaka, visit_date__month__lte=12).values_list('facility__countyy').annotate(totalvisits=Count('id')).order_by('-totalvisits')
			quarter_visits_total = Visit.objects.filter(visit_date__year__gte=mwaka, visit_date__month__gte=10, visit_date__year__lte=mwaka, visit_date__month__lte=12).count()


		context = {
			'miaka' : miaka,
			'mwaka' : mwaka,
			'quarter' : quarter,
			'quarter_visits' : quarter_visits,
			'quarter_visits_total' : quarter_visits_total
		}

		template = "reporting/quarter-visits.html"

	return render(request, template, context)








# check facility by county distribution
@login_required(login_url='login')
def county_facility_distribution(request, county, mwezi, mwaka):
	county = get_object_or_404(Counties, pk=county)
	mwezi = mwezi
	mwaka = mwaka

	facilities = Nets_distributed.objects.filter(facility__countyy=county, date_issued__year=mwaka, date_issued__month=mwezi).order_by('nets_issued')
	total_nets_delivered = Nets_distributed.objects.filter(facility__countyy=county, date_issued__year=mwaka, date_issued__month=mwezi).aggregate(Sum('nets_issued'))
	template = "reporting/county-facility-dist.html"

	context = {
		'facilities' : facilities,
		'mwezi' : mwezi,
		'mwaka' : mwaka,
		'total_nets_delivered' : total_nets_delivered
	}

	return render(request, template, context)


# CSV DOWNLOADS
# Export county visits by month
@login_required(login_url='login')
def export_monthly_county_visits(request, mwezi, mwaka):

	mwezii = calendar.month_abbr[int(mwezi)]
	file_name = "{}_{}_monthly_county_visits.csv".format(mwezii, mwaka)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename='+file_name

	writer = csv.writer(response)
	writer.writerow(['County', 'Facility visits'])

	reports = Visit.objects.filter(visit_date__year=mwaka, visit_date__month=mwezi).values_list('facility__countyy').annotate(totalvisits=Count('id')).order_by('-totalvisits')
	for report in reports:
	    writer.writerow(report)

	return response


# AUTOCOMPLETE
# Sub county live search
@login_required(login_url='login')
def subcounty_autocomplete(request,*args,**kwargs):
    data = request.GET
    sub_county = data.get("term")
    if sub_county:
        sub_counties = Facilities.objects.filter(status=1, facility_name__startswith = facility).values('sub_county').distinct()
        results = []
        for s_county in sub_counties:
            s_county_json = {}
            s_county_json['label'] = s_county.sub_county
            results.append(s_county_json)
        data = json.dumps(results)
    else:
        facilities = Facilities.objects.values('sub_county').distinct()
        results = []
        for s_county in sub_counties:
            hosi_json = {}
            hosi_json['label'] = s_county.sub_county
            results.append(hosi_json)
        data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
