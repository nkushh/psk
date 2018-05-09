import datetime, calendar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pyexcel as pe
from .models import Nets_distributed, Distribution_report, Warehouse, Stocking_history
from facilities.models import Counties, Facilities

# Loads distribution dashboard template
@login_required(login_url='login')
def distribution_index(request):
	today = datetime.datetime.now()
	mwaka = today.year
	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))

	facilities = Facilities.objects.all()  
	recently_distributed = Nets_distributed.objects.filter(date_issued__month=today.month) 
	context = {
		'facilities' : facilities,
		'recently_distributed' : recently_distributed
	}
	template = "distribution/index.html"
	return render(request, template, context)

# Fetch nets issued to facilities month and year
@login_required(login_url='login')
def nets_issued_to_facilities(request):
	today = datetime.datetime.now()
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
		'page_range' : page_range
	}
	return render(request, template, context)

# record nets issued to a facility
@login_required(login_url='login')
def record_nets_issued(request):
	if request.method=="POST":
		facility = get_object_or_404(Facilities, facility_name=request.POST['facility'])
		nets_issued = record['nets_issued']
		donor = record['donor']
		invoice_no = record['invoice_no']
		warehouse = record['warehouse']
		date_issued = record['date_issued']
		invoice_no = record['invoice_no']
		# request_id = request.POST['request_id']
		# transporter = request.POST['transporter']

		issued = Nets_distributed(facility=facility, invoice_no=invoice_no, nets_issued=nets_issued, donor=donor, date_issued=date_issued).save()
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


# NETS DISTRIBUTION TO TARGET GROUP REPORT MODULE
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
				bal_bf = record['bal_bf']
				anc_nets = record['anc_nets']
				cwc_nets = record['cwc_nets']
				others_nets = record['others_nets']
				total_nets = int(anc_nets)+int(cwc_nets)+int(others_nets)
				bal_cf = record['bal_cf']

				if confirm_nets_issuance(total_nets, facility.net_balance, facility.system_net_balance):
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

					facility.net_balance = bal_cf
					facility.system_net_balance = facility.system_net_balance - total_nets
					facility.save()

				else:
					messages.error(request, "Error! Nets issued for {}, exceed the remaining balance!".format(facility))
					return redirect("distribution:record_distribution")
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
	today = datetime.datetime.now()
	records = Distribution_report.objects.all()
	# facility = get_object_or_404(Facilities, pk=34)
	# amc = Distribution_report.objects.filter(facility=facility).values('facility').aggregate(totalnets=Sum('total_nets'))
	# sc_recently_distributed = Nets_distributed.objects.filter(facility__sub_county="Kajiado Central")

	template = "distribution/distribution-records.html"
	context = {
		'records' : records
	}
	return render(request, template, context)

# Fetch nets issued to cwc and anc for current month and year
@login_required(login_url='login')
def nets_distributed_by_county(request):
	today = datetime.datetime.now()
	records = Distribution_report.objects.values('facility__county').annotate(Sum('total_nets')).distinct()

	template = "distribution/counties-issuance.html"
	context = {
		'records' : records
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

		if confirm_nets_issuance(total_nets, facility.net_balance, facility.system_net_balance):

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

			facility.net_balance = bal_cf
			facility.system_net_balance = facility.system_net_balance - total_nets
			facility.save()
			messages.success(request, "Success! Nets distribution for {} {} successfully recorded.".format(facility.facility_name, dist_month))
			return redirect('distribution:nets_distributed')
		else:
			messages.error(request, "Error! Nets issued exceed the remaining balance!")
			return redirect("distribution:record_distribution")
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
















