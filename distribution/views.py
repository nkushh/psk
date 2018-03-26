import datetime, calendar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pyexcel as pe
from .models import Nets_distributed, Distribution_report
from facilities.models import Facilities

# Loads distribution dashboard template
@login_required(login_url='login')
def distribution_index(request):
	today = datetime.datetime.now()

	context = {
		'facilities' : Facilities.objects.all(),
		'recently_distributed' : Nets_distributed.objects.filter(date_issued__month=today.month),
	}
	template = "distribution/index.html"
	return render(request, template, context)

# Fetch nets issued to facilities month and year
@login_required(login_url='login')
def nets_issued_to_facilities(request):
	today = datetime.datetime.now()
	recently_delivered = Nets_distributed.objects.all()

	template = "distribution/delivery-records.html"
	context = {
		'recently_delivered' : recently_delivered
	}
	return render(request, template, context)

# record nets issued to a facility
@login_required(login_url='login')
def record_nets_issued(request):
	if request.method=="POST":
		facility = get_object_or_404(Facilities, facility_name=request.POST['facility'])
		nets_issued = request.POST['nets_issued']
		date_issued = request.POST['date_issued']
		invoice_no = request.POST['invoice_no']
		# request_id = request.POST['request_id']
		# transporter = request.POST['transporter']

		issued = Nets_distributed(facility=facility, invoice_no=invoice_no, nets_issued=nets_issued, date_issued=date_issued).save()
		messages.success(request, "Success! Nets issuance to {} successfully recorded.".format(facility.facility_name))
		return redirect('distribution:nets_distribution')
	else:
		template = "distribution/record-issuance.html"
		context={}
		return render(request, template, context)

# Fetch nets issued to cwc and anc for current month and year
@login_required(login_url='login')
def nets_distributed(request):
	today = datetime.datetime.now()
	records = Distribution_report.objects.all()
	facility = get_object_or_404(Facilities, pk=34)
	amc = Distribution_report.objects.filter(facility=facility).values('facility').aggregate(totalnets=Sum('total_nets'))

	template = "distribution/distribution-records.html"
	context = {
		'records' : records,
		'amc' : amc,
	}
	return render(request, template, context)

# Record the monthly net issuance report from facilities
@login_required(login_url='login')
def record_distribution(request):
	today = datetime.datetime.now()

	if request.method=="POST":
		facility = get_object_or_404(Facilities, facility_name=request.POST['facility'])
		dist_month = request.POST['dist_month']
		dist_year = request.POST['dist_year']
		bal_cf = request.POST['bal_cf']
		bal_bf = request.POST['bal_bf']
		anc_nets = request.POST['anc_nets']
		cwc_nets = request.POST['cwc_nets']
		others_nets = request.POST['others_nets']

		total_nets = int(anc_nets)+int(cwc_nets)+int(others_nets)

		distribution = Distribution_report(
				facility=facility, 
				dist_month=dist_month, 
				dist_year=dist_year, 
				bal_bf=bal_bf, 
				cwc_nets=cwc_nets, 
				anc_nets=anc_nets, 
				others_nets=others_nets,
				total_nets=total_nets,
				bal_cf=bal_cf
				).save()
		messages.success(request, "Success! Nets distribution for {} {} successfully recorded.".format(facility.facility_name, dist_month))
		return redirect('distribution:nets_distributed')
	else:
		template = "distribution/record-distribution.html"
		context = {
			'facilities' : Facilities.objects.all(),
			'miaka' : range(2000, today.year+1),
		}
		return render(request, template, context)


