import datetime, calendar, csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db.models.functions import Extract, TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pyexcel as pe
from authentication.models import UserProfile
from .models import Distribution_report, Distribution_target, Nets_distributed, Nets_donated, Stocking_history, Warehouse
from facilities.models import Counties, Epidemiological_zones, Facilities, Regions

# Loads distribution dashboard template
@login_required(login_url='login')
def distribution_index(request):
	today = datetime.datetime.now()

	if today.month < 2:
		mwaka = today.year - 1
	else:
		mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	county_distribution = Nets_distributed.objects.values('facility__county').annotate(county_total=Sum('nets_issued')).order_by('-county_total') 
	distribution_by_ez = Nets_distributed.objects.values('facility__epidemiological_zone').annotate(ez_distribution=Sum('nets_issued')).order_by('-ez_distribution')
	region_distribution = Nets_distributed.objects.values('facility__psk_region').annotate(region_total=Sum('nets_issued')).order_by('-region_total')
	total_nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka).aggregate(nets=Sum('nets_issued'))
	total_facilities_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka).values('facility').annotate(Count('facility')).distinct()
	total_nets_issued = Distribution_report.objects.aggregate(issued_nets=Sum('total_nets'))
	total_nets_donated = Nets_donated.objects.aggregate(donated_nets=Sum('nets_issued'))
	# Filters
	counties = Counties.objects.order_by('county_name')
	regions = Regions.objects.order_by('region_name')

	context = {
		'counties' : counties,
		'county_distribution' : county_distribution,
		'distribution_by_ez' : distribution_by_ez,
		'months_choices' : months_choices,
		'regions' : regions,
		'region_distribution' : region_distribution,
		'total_facilities_delivered' : total_facilities_delivered,
		'total_nets_delivered' : total_nets_delivered,
		'total_nets_donated' : total_nets_donated,
		'total_nets_issued' : total_nets_issued
	}
	template = "distribution/index.html"
	return render(request, template, context)

# Fetch month nets delivery
@login_required(login_url='login')
def monthly_net_delivery(request, mwezi):
	today = datetime.datetime.now()

	if today.month < 2:
		mwaka = today.year - 1
	else:
		mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	county_distribution = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).values('facility__county').annotate(county_total=Sum('nets_issued')).order_by('-county_total') 
	distribution_by_ez = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).values('facility__epidemiological_zone').annotate(ez_distribution=Sum('nets_issued')).order_by('-ez_distribution')
	region_distribution = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).values('facility__psk_region').annotate(region_total=Sum('nets_issued')).order_by('-region_total')
	total_nets_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).aggregate(nets=Sum('nets_issued'))
	total_facilities_delivered = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).annotate(Count('facility', distinct=True))
	total_nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).aggregate(issued_nets=Sum('total_nets'))
	total_nets_donated = Nets_donated.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).aggregate(donated_nets=Sum('nets_issued'))
	# Accompaniements
	counties = Counties.objects.order_by('county_name')
	regions = Regions.objects.order_by('region_name')
	query_month = calendar.month_name[int(mwezi)]

	context = {
		'counties' : counties,
		'county_distribution' : county_distribution,
		'distribution_by_ez' : distribution_by_ez,
		'months_choices' : months_choices,
		'mwezi' : mwezi,
		'mwaka' : mwaka,
		'query_month' : query_month,
		'regions' : regions,
		'region_distribution' : region_distribution,
		'total_facilities_delivered' : total_facilities_delivered,
		'total_nets_delivered' : total_nets_delivered,
		'total_nets_issued' : total_nets_issued,
		'total_nets_donated' : total_nets_donated

	}
	template = "distribution/index.html"
	return render(request, template, context)	

# Fetch nets issued to facilities month and year
@login_required(login_url='login')
def nets_issued_to_facilities(request):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)
	counties = Facilities.objects.values('county').distinct()
	regions = Regions.objects.all()
	if account_profile.usertype=="Coordinator":
		recently_delivered = Nets_distributed.objects.filter(facility__psk_region=account_profile.psk_region)
	else:
		recently_delivered = Nets_distributed.objects.all()
	
	

	page = request.GET.get('page', 1)

	paginator = Paginator(recently_delivered, 50)

	try:
		recently_delivered = paginator.page(page)
	except PageNotAnInteger:
		recently_delivered = paginator.page(1)
	except EmptyPage:
		recently_delivered = paginator.page(paginator.num_pages)

	index = recently_delivered.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	template = "distribution/delivery-records.html"
	context = {
		'recently_delivered' : recently_delivered,
		'page_range' : page_range,
		'counties' : counties,
		'regions' : regions
	}
	return render(request, template, context)

@login_required(login_url='login')
def nets_donated(request):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)
	counties = Facilities.objects.values('county').distinct()
	regions = Regions.objects.all()
	if account_profile.usertype=="Coordinator":
		recently_delivered = Nets_donated.objects.filter(facility__psk_region=account_profile.psk_region)
	else:
		recently_delivered = Nets_donated.objects.order_by('-date_issued')
	
	

	page = request.GET.get('page', 1)

	paginator = Paginator(recently_delivered, 50)

	try:
		recently_delivered = paginator.page(page)
	except PageNotAnInteger:
		recently_delivered = paginator.page(1)
	except EmptyPage:
		recently_delivered = paginator.page(paginator.num_pages)

	index = recently_delivered.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	template = "distribution/donations-records.html"
	context = {
		'recently_delivered' : recently_delivered,
		'page_range' : page_range,
		'counties' : counties,
		'regions' : regions
	}
	return render(request, template, context)

@login_required(login_url='login')
def delivery_by_county(request, county):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)
	counties = Facilities.objects.values('county').distinct()
	regions = Regions.objects.all()

	recently_delivered = Nets_distributed.objects.filter(facility__county=county).order_by('-date_issued')
	nets_delivered = Nets_distributed.objects.filter(facility__county=county).aggregate(total_nets=Sum('nets_issued'))
	
	

	page = request.GET.get('page', 1)

	paginator = Paginator(recently_delivered, 50)

	try:
		recently_delivered = paginator.page(page)
	except PageNotAnInteger:
		recently_delivered = paginator.page(1)
	except EmptyPage:
		recently_delivered = paginator.page(paginator.num_pages)

	index = recently_delivered.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	template = "distribution/delivery-records.html"
	context = {
		'recently_delivered' : recently_delivered,
		'page_range' : page_range,
		'nets_delivered' : nets_delivered,
		'counties' : counties,
		'regions' : regions,
		'county' : county
	}
	return render(request, template, context)


@login_required(login_url='login')
def delivery_by_region(request, region):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)
	counties = Facilities.objects.values('county').distinct()
	regions = Regions.objects.all()

	recently_delivered = Nets_distributed.objects.filter(facility__psk_region=region).order_by('-date_issued')
	nets_delivered = Nets_distributed.objects.filter(facility__psk_region=region).aggregate(total_nets=Sum('nets_issued'))
	
	

	page = request.GET.get('page', 1)

	paginator = Paginator(recently_delivered, 50)

	try:
		recently_delivered = paginator.page(page)
	except PageNotAnInteger:
		recently_delivered = paginator.page(1)
	except EmptyPage:
		recently_delivered = paginator.page(paginator.num_pages)

	index = recently_delivered.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	template = "distribution/delivery-records.html"
	context = {
		'recently_delivered' : recently_delivered,
		'page_range' : page_range,
		'counties' : counties,
		'regions' : regions,
		'nets_delivered' : nets_delivered,
		'regionn' : region
	}
	return render(request, template, context)

# record nets issued to a facility
@login_required(login_url='login')
def record_nets_issued(request):
	if request.method=="POST":
		facility = get_object_or_404(Facilities, mfl_code=request.POST['facility'])
		nets_issued = request.POST['nets_issued']
		donor = request.POST['donor']
		invoice_no = request.POST['invoice_no']
		warehouse = request.POST['warehouse']
		date_issued = request.POST['date_issued']
		invoice_no = request.POST['invoice_no']
		# request_id = request.POST['request_id']
		# transporter = request.POST['transporter']

		issued = Nets_distributed(facility=facility, invoice_no=invoice_no, nets_issued=nets_issued, donor_code=donor, date_issued=date_issued).save()
		facility.net_balance = int(nets_issued) + int(facility.net_balance)
		facility.save()
		messages.success(request, "Success! Nets issuance to {} successfully recorded.".format(facility.facility_name))
		return redirect('distribution:nets_to_facilities')
	else:
		template = "distribution/record-issuance.html"
		context={}
		return render(request, template, context)

# record nets issued to a facility excel upload
@login_required(login_url='login')
def record_nets_issued_excel(request):
	if request.method=='POST' and request.FILES['excel_file']:
		myfile = request.FILES['excel_file']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		missing_facilities = []

		records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
		for record in records:
			if Facilities.objects.filter(mfl_code=record['facility']).exists():
				facility = get_object_or_404(Facilities, mfl_code=record['facility'])
				invoice_no = record['invoice']
				warehouse = record['warehouse']
				nets_issued = record['nets']
				donor = record['donor']
				date_issued = record['date_issued']
			else:
				missing_facilities.append(record['facility'])
				continue

			issued = Nets_distributed(facility=facility, invoice_no=invoice_no, nets_issued=nets_issued, donor_code=donor, date_issued=date_issued).save()
			facility.net_balance = int(nets_issued) + int(facility.net_balance)
			facility.system_net_balance = int(nets_issued) + int(facility.system_net_balance)
			facility.save()

		messages.success(request, "Success! Nets issuance successfully recorded.")
		request.session['missing_facilities'] = missing_facilities
		return redirect('distribution:nets_to_facilities')
	else:
		template = "distribution/excel-issuance.html"
		context={}
		return render(request, template, context)

@login_required(login_url='login')
def record_nets_donated_excel(request):
	if request.method=='POST' and request.FILES['excel_file']:
		myfile = request.FILES['excel_file']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		missing_facilities = []

		records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
		for record in records:
			beneficiary =record['beneficiary']
			invoice_no = record['invoice']
			warehouse = record['warehouse']
			nets_issued = record['nets']
			donor = record['donor']
			date_issued = record['date_issued']
			if Nets_donated.objects.filter(invoice_no=invoice_no).exists():
				continue

			issued = Nets_donated(beneficiary=beneficiary, invoice_no=invoice_no, nets_issued=nets_issued, donor_code=donor, date_issued=date_issued).save()


		messages.success(request, "Success! Nets donated records successfully saved.")
		return redirect('distribution:nets_donated')
	else:
		template = "distribution/excel-donation.html"
		context={}
		return render(request, template, context)

@login_required(login_url='login')
def download_all_distribution_excel(request):
	today = datetime.datetime.now()

	if today.month < 2:
		mwaka = today.year - 1
	else:
		mwaka = today.year

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="distribution.csv"'

	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])

	reports = Nets_distributed.objects.filter(date_issued__year=mwaka).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	for report in reports:
	    writer.writerow(report)

	return response

@login_required(login_url='login')
def download_distribution_excel(request, mwaka, mwezi):
	today = datetime.datetime.now()

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="distribution.csv"'

	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])

	reports = Nets_distributed.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	for report in reports:
	    writer.writerow(report)

	return response

@login_required(login_url='login')
def download_issuance_excel(request, mwezi, mwaka):
	today = datetime.datetime.now()

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="nets_issued.csv"'

	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])

	reports = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).values_list('facility__county').annotate(totalnets=Sum('total_nets')).order_by('-totalnets')
	for report in reports:
	    writer.writerow(report)

	return response

def download_qdistribution_excel(request):
	today = datetime.datetime.now()

	if request.method == "POST":
		quarter = request.POST['quarter']
		mwaka = request.POST['mwaka']


	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="distribution.csv"'

	writer = csv.writer(response)
	writer.writerow(['County', 'Nets Issued'])
	if quarter == "One":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=1, date_issued__year__lte=mwaka, date_issued__month__lte=3).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Two":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=4, date_issued__year__lte=mwaka, date_issued__month__lte=6).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Three":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=7, date_issued__year__lte=mwaka, date_issued__month__lte=9).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')
	elif quarter == "Four":
		quarter_dist = Nets_distributed.objects.filter(date_issued__year__gte=mwaka, date_issued__month__gte=10, date_issued__year__lte=mwaka, date_issued__month__lte=12).values_list('facility__county').annotate(totalnets=Sum('nets_issued')).order_by('-totalnets')

	for report in quarter_dist:
	    writer.writerow(report)

	return response
	

# Delete all the net delivery records in the database.
# Super admin only
@login_required(login_url='login')
def delete_all_deliveries(request):
    deliveries = Nets_distributed.objects.all()
    deliveries.delete()
    return redirect("distribution:nets_to_facilities")

@login_required(login_url='login')
def delete_delivery(request, delivery_pk):
    delivery = get_object_or_404(Nets_distributed, pk=delivery_pk)
    delivery.delete()
    messages.success(request, "Success! Delivery recorded successfully deleted.")
    return redirect("distribution:nets_to_facilities")

# Reset all the net balances to zero in the database.
# Super admin only
@login_required(login_url='login')
def reset_nets_balance(request):
	for record in Facilities.objects.all():
		record.net_balance = 0
		record.system_net_balance = 0
		record.save()
	return redirect("facilities:facilities")


# NETS ISSUED TO TARGET GROUP REPORT MODULE
# Loads issuance dashboard template
@login_required(login_url='login')
def issuance_index(request):
	today = datetime.datetime.now()
	
	if today.month < 2:
		mwaka = today.year - 1
	else:
		mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	county_issuance = Distribution_report.objects.values('facility__county').annotate(county_total=Sum('total_nets')).order_by('-county_total') 
	issuance_by_ez = Distribution_report.objects.values('facility__epidemiological_zone').annotate(ez_issuance=Sum('total_nets')).order_by('-ez_issuance')
	region_issuance = Distribution_report.objects.values('facility__psk_region').annotate(region_total=Sum('total_nets')).order_by('-region_total')
	total_nets_issued = Distribution_report.objects.filter(dist_year=mwaka).aggregate(nets=Sum('total_nets'))
	total_facilities_issued = Distribution_report.objects.filter(dist_year=mwaka).values('facility').annotate(Count('facility')).distinct()
	# total_nets_issued = Distribution_report.objects.aggregate(issued_nets=Sum('total_nets'))
	total_nets_donated = Nets_donated.objects.aggregate(donated_nets=Sum('nets_issued'))
	# Filters
	counties = Counties.objects.order_by('county_name')
	regions = Regions.objects.order_by('region_name')

	context = {
		'counties' : counties,
		'county_issuance' : county_issuance,
		'issuance_by_ez' : issuance_by_ez,
		'months_choices' : months_choices,
		'regions' : regions,
		'region_issuance' : region_issuance,
		'total_facilities_issued' : total_facilities_issued,
		'total_nets_issued' : total_nets_issued,
		'total_nets_donated' : total_nets_donated
	}
	template = "distribution/index2.html"
	return render(request, template, context)

@login_required(login_url='login')
def monthly_issuance_index(request, mwezi):
	today = datetime.datetime.now()
	
	if today.month < 2:
		mwaka = today.year - 1
	else:
		mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	county_issuance = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).values('facility__county').annotate(county_total=Sum('total_nets')).order_by('-county_total') 
	issuance_by_ez = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).values('facility__epidemiological_zone').annotate(ez_issuance=Sum('total_nets')).order_by('-ez_issuance')
	region_issuance = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).values('facility__psk_region').annotate(region_total=Sum('total_nets')).order_by('-region_total')
	total_nets_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).aggregate(nets=Sum('total_nets'))
	total_facilities_issued = Distribution_report.objects.filter(dist_year=mwaka, dist_month=mwezi).values('facility').annotate(Count('facility')).distinct()
	# total_nets_issued = Distribution_report.objects.aggregate(issued_nets=Sum('total_nets'))
	total_nets_donated = Nets_donated.objects.filter(date_issued__year=mwaka, date_issued__month=mwezi).aggregate(donated_nets=Sum('nets_issued'))
	# Filters
	counties = Counties.objects.order_by('county_name')
	regions = Regions.objects.order_by('region_name')
	query_month = calendar.month_abbr[int(mwezi)]

	context = {
		'counties' : counties,
		'county_issuance' : county_issuance,
		'issuance_by_ez' : issuance_by_ez,
		'months_choices' : months_choices,
		'mwaka' : mwaka,
		'mwezi' : mwezi,
		'query_month' : query_month,
		'regions' : regions,
		'region_issuance' : region_issuance,
		'total_facilities_issued' : total_facilities_issued,
		'total_nets_issued' : total_nets_issued,
		'total_nets_donated' : total_nets_donated
	}
	template = "distribution/index2.html"
	return render(request, template, context)

# record nets issued to pregnant women and children under one year upload
@login_required(login_url='login')
def record_nets_distributed_excel(request):
	if request.method=='POST' and request.FILES['excel_file']:
		myfile = request.FILES['excel_file']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		missing_facilities = []

		records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
		for record in records:
			if Facilities.objects.filter(mfl_code=record['facility']).exists():
				facility = get_object_or_404(Facilities, mfl_code=record['facility'])
				dist_month = record['dist_month']
				dist_year = record['dist_year']
				anc_nets = int(record['anc_nets'])
				cwc_nets = int(record['cwc_nets'])
				others_nets = int(record['others_nets'])

				total_nets = anc_nets + cwc_nets + others_nets
				bal_cf = int(record['bal_cf'])

				# if confirm_nets_issuance(total_nets, facility.net_balance, facility.system_net_balance):
				distribution = Distribution_report(
						facility=facility, 
						dist_month=dist_month, 
						dist_year=dist_year,
						cwc_nets=cwc_nets, 
						anc_nets=anc_nets, 
						others_nets=others_nets,
						total_nets=total_nets,
						bal_cf=bal_cf
						).save()

				facility.net_balance = bal_cf
				facility.system_net_balance = facility.system_net_balance - total_nets
				facility.save()

				# else:
				# 	messages.error(request, "Error! Nets issued for {}, exceed the remaining balance!".format(facility))
				# 	return redirect("distribution:record_distribution")
			else:
				missing_facilities.append(record['facility'])
				continue

		messages.success(request, "Success! Nets distribution reports successfully recorded.")
		request.session['missing_facilities'] = missing_facilities
		return redirect('distribution:nets_distributed')

	else:
		template = "distribution/excel-distribution.html"
		context={}
		return render(request, template, context)

# Fetch nets issued to cwc and anc for current month and year
@login_required(login_url='login')
def nets_distributed(request):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)
	if account_profile.usertype!="Admin":
		records = Distribution_report.objects.filter(facility__psk_region=account_profile.psk_region).order_by('-dist_month')
	else:
		records = Distribution_report.objects.all().order_by('-dist_month')

	page = request.GET.get('page', 1)

	paginator = Paginator(records, 50)

	try:
		records = paginator.page(page)
	except PageNotAnInteger:
		records = paginator.page(1)
	except EmptyPage:
		records = paginator.page(paginator.num_pages)

	index = records.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	template = "distribution/distribution-records.html"
	context = {
		'page_range' : page_range,
		'records' : records
	}
	return render(request, template, context)

# Fetch nets issued to cwc and anc per county
@login_required(login_url='login')
def nets_distributed_by_county(request):
	today = datetime.datetime.now()
	records = Distribution_report.objects.values('facility__county').annotate(total_issued=Sum('total_nets')).order_by('-total_issued')

	template = "distribution/counties-issuance.html"
	context = {
		'records' : records
	}
	return render(request, template, context)

# Record the monthly net issuance report for single facilities
@login_required(login_url='login')
def record_distribution(request):
	today = datetime.datetime.now()

	if request.method=="POST":
		facility = get_object_or_404(Facilities, mfl_code=request.POST['facility'])
		dist_month = request.POST['dist_month']
		dist_year = request.POST['dist_year']
		bal_cf = request.POST['bal_cf']
		anc_nets = request.POST['anc_nets']
		cwc_nets = request.POST['cwc_nets']
		others_nets = request.POST['others_nets']

		total_nets = int(anc_nets)+int(cwc_nets)+int(others_nets)

		# if confirm_nets_issuance(total_nets, facility.net_balance, facility.system_net_balance):

		distribution = Distribution_report(
				facility=facility, 
				dist_month=dist_month, 
				dist_year=dist_year, 
				cwc_nets=cwc_nets, 
				anc_nets=anc_nets, 
				others_nets=others_nets,
				total_nets=total_nets,
				bal_cf=bal_cf
				).save()

		facility.net_balance = bal_cf
		facility.system_net_balance = facility.system_net_balance - total_nets
		facility.save()
		messages.success(request, "Success! Nets distribution for {} {} successfully recorded.".format(facility.facility_name, dist_month))
		return redirect('distribution:nets_distributed')
		# else:
		# 	messages.error(request, "Error! Nets issued exceed the remaining balance!")
		# 	return redirect("distribution:record_distribution")
	else:
		today = datetime.datetime.now()
		mwaka = today.year
		months_choices = []
		for i in range(1,13):
		    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

		template = "distribution/record-distribution.html"
		context = {
			'facilities' : Facilities.objects.all(),
			'miaka' : range(2000, today.year+1),
			'months_choices' : months_choices
		}
		return render(request, template, context)


def confirm_nets_issuance(total_nets, net_balance, system_net_balance):
	if total_nets > net_balance or total_nets > system_net_balance:
		return False
	else:
		return True


###############################################################################################################################
# CRUD functions for distribution targets
@login_required(login_url='login')
def create_target(request):
    if request.method == "POST":
        target_month = request.POST['target_month']
        target_year = request.POST['target_year']
        donor = request.POST['donor'].upper()
        target = request.POST['target']
        
        if Distribution_target.objects.filter(target_month=target_month, target_year=target_year, donor=donor).exists():
            messages.error(request, "Target details were not saved. That target exists. Try again!")
            return redirect("distribution:create_target")
        else:
        	set_target = Distribution_target(target_month=target_month, target_year=target_year, donor=donor, target=target).save()
        	messages.success(request, "Target added successfully!")
        	return redirect("distribution:fetch_targets")
    else:
    	today = datetime.datetime.now()
    	mwaka = today.year
    	months_choices = []
    	for i in range(1,13):
    		months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

    	context = {
    		'months_choices' : months_choices,
    		'miaka' : range(mwaka, mwaka+2)
    	}

    	template = "distribution/distribution-target.html"

    	return render(request, template, context)

@login_required(login_url='login')
def fetch_targets(request):
	today = datetime.datetime.now()
	if today.month==1 and today.day < 15:
		mwaka = today.year - 1
	else:
		mwaka = today.year

	overall_achieved = Nets_distributed.objects.filter(date_issued__year=mwaka, donor_code='USAID').aggregate(total_distributed=Sum('nets_issued'))
	overall_target = Distribution_target.objects.filter(target_year=mwaka).aggregate(target_total=Sum('target'))
	targets = Distribution_target.objects.filter(target_year=mwaka).order_by('target_month')
	targets_graph = Distribution_target.objects.filter(target_year=mwaka).values('target_month', 'target').order_by('target_month')
	achieved = Nets_distributed.objects.filter(date_issued__year=mwaka, donor_code='USAID').annotate(mwezi=Extract('date_issued', 'month')).values('mwezi').annotate(total_achieved=Sum('nets_issued')).order_by('mwezi')
	
	# Convert month to string
	for i in targets:
		i.target_month = calendar.month_abbr[i.target_month]
	for i in targets_graph:
		i['target_month'] = calendar.month_abbr[i['target_month']]
	for m in achieved:
		m['mwezi'] = calendar.month_abbr[m['mwezi']]

	# Achieved target percentage
	achieved_percentage = (overall_achieved['total_distributed']*100)/overall_target['target_total']

	context = {
		'achieved' : achieved,
		'achieved_percentage' : achieved_percentage,
		'mwaka' : mwaka,
		'overall_achieved' : overall_achieved,
		'overall_target' : overall_target,
		'targets' : targets,
		'targets_graph' : targets_graph
	}

	template = "distribution/targets.html"
	return render(request, template, context)





###############################################################################################################################
# WAREHOUSE
@login_required(login_url='login')
def all_warehouses(request):
	warehouses = Warehouse.objects.all().order_by('-warehouse_name')
	template = "distribution/warehouses.html"
	context = {
		'warehouses' : warehouses
	}

	return render(request, template, context)


@login_required(login_url='login')
def new_warehouse(request):
	if request.method=="POST":
		warehouse_name = request.POST['warehouse_name']
		county = get_object_or_404(Counties, pk=request.POST['county'])
		location = request.POST['location']
		contact_person = request.POST['contact_person']
		contact = request.POST['contact']

		if Warehouse.objects.filter(warehouse_name=warehouse_name).exists():
			messages.error(request, "Error! A warehouse with the name {} already exists".format(warehouse_name))
			return redirect("distribution:new_warehouse")
		else:
			Warehouse(warehouse_name=warehouse_name, county=county, location=location, contact_person=contact_person, contact=contact).save()
			messages.success(request, "Success! {} details successfully added.".format(warehouse_name))
			return redirect("distribution:new_warehouse")
	else:
		template = "distribution/new-warehouse.html"
		context = {
			"counties" : Counties.objects.all().order_by('county_name')
		}
		return render(request, template, context)


# Stock warehouse
@login_required(login_url='login')
def stock_warehouse(request):
	if request.method=="POST":
		warehouse = get_object_or_404(Warehouse, pk=request.POST['warehouse'])
		donor = request.POST['donor']
		nets_quantity = int(request.POST['nets_quantity'])
		date_stocked = request.POST['date_stocked']

		warehouse.stock_balance = warehouse.stock_balance + nets_quantity
		warehouse.save()

		Stocking_history(warehouse=warehouse, donor=donor, nets_quantity=nets_quantity, date_stocked=date_stocked).save()
		messages.success(request, "Success! {} stock added successfully.".format(warehouse.warehouse_name))
		return redirect("distribution:stocking_history")
	else:
		template = "distribution/stock-warehouse.html"
		context = {
			"warehouses" : Warehouse.objects.all().order_by('warehouse_name')
		}
		return render(request, template, context)


@login_required(login_url='login')
def stockin_history(request):
	context = {
		"stocks" : Stocking_history.objects.all().order_by('-date_stocked')
	}
	template = "distribution/stocking-history.html"
	return render(request, template, context)
















