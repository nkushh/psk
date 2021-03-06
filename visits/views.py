from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import UserProfile
from facilities.models import Facilities
from distribution.models import Distribution_report
from .models import Visit
from .forms import NewVisitForm
import datetime, calendar, csv
import pyexcel as pe

# Create your views here.
@login_required(login_url='login')
def visits_index(request):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)

	today = datetime.datetime.now()
	this_mwaka = today.year
	this_month = today.month
	last_month = today.month - 1

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(this_mwaka, i, 1).strftime('%B')))

	if account_profile.usertype == "Field Assistant":
		recently_visited = Visit.objects.filter(supervisor=account).order_by('-visit_date')
		total_visits = Visit.objects.filter(supervisor=account).count()
		current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month, supervisor=account).count()
		monthly_visits = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
		risk_status = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).values('risk_level').annotate(status_count=Count('id'))
		previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month, supervisor=account).count()
		field_assistants = UserProfile.objects.filter(usertype="Field Assistant")

	elif account_profile.usertype == "Coordinator":
		recently_visited = Visit.objects.filter(supervisor=account).order_by('-visit_date')
		total_visits = Visit.objects.filter(supervisor=account).count()
		current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month, supervisor=account).count()
		monthly_visits = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
		risk_status = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).values('risk_level').annotate(status_count=Count('id'))
		previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month, supervisor=account).count()
		field_assistants = UserProfile.objects.filter(usertype="Field Assistant", psk_region=account_profile.psk_region)
	elif account_profile.usertype == "Admin":
		recently_visited = Visit.objects.all().order_by('-visit_date')
		total_visits = Visit.objects.count()
		current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month).count()
		monthly_visits = Visit.objects.filter(visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
		risk_status = Visit.objects.filter(visit_date__year=this_mwaka).values('risk_level').annotate(status_count=Count('id'))
		previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month).count()
		field_assistants = UserProfile.objects.filter(usertype="Field Assistant")
		coordinators = UserProfile.objects.filter(usertype="Coordinator")

	miaka = range(2018,this_mwaka+1)
	mwezi_huu = calendar.month_name[int(this_month)]
	mwezi_uliopita = calendar.month_name[int(last_month)]
	coordinators = UserProfile.objects.filter(usertype="Coordinator")
	less_ten = Visit.objects.filter(months_of_stock__range=(0, 10)).count()
	less_thirty = Visit.objects.filter(months_of_stock__range=(10, 30)).count()
	less_sixty = Visit.objects.filter(months_of_stock__range=(30, 60)).count()
	less_hundred = Visit.objects.filter(months_of_stock__range=(60, 100)).count()
	try:
	    page = request.GET.get('page', 1)
	except:
	    page = 1

	paginator = Paginator(recently_visited, 50)

	try:
	    recently_visited = paginator.page(page)
	except PageNotAnInteger:
	    recently_visited = paginator.page(1)
	except EmptyPage:
	    recently_visited = paginator.page(paginator.num_pages)

	index = recently_visited.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	context = {
		'coordinators' : coordinators,
		'current_month' : current_month,
		'field_assistants' : field_assistants,
		'miaka' : miaka,
		'months_choices' : months_choices,
		'monthly_visits' : monthly_visits,
		'mwezi_huu' : mwezi_huu,
		'mwezi_uliopita' : mwezi_uliopita,
		'previous_month' : previous_month,
		'recently_visited' : recently_visited,
		'risk_status' : risk_status,
		'total_visits' : total_visits,
		'page_range' : page_range,
		'less_ten' : less_ten,
		'less_thirty' : less_thirty,
		'less_sixty' : less_sixty,
		'less_hundred' : less_hundred

	}
	template = "visits/index.html"
	return render(request, template, context)

@login_required(login_url='login')
def list_view(request):
	account = request.user
	account_profile = get_object_or_404(UserProfile, user=account)

	today = datetime.datetime.now()
	this_mwaka = today.year
	this_month = today.month
	last_month = today.month - 1

	miaka = range(2018,this_mwaka+1)
	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(this_mwaka, i, 1).strftime('%B')))

	if account_profile.usertype == "Field Assistant":
		recently_visited = Visit.objects.filter(supervisor=account).order_by('-date_recorded')
		total_visits = Visit.objects.filter(supervisor=account).count()
		current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month, supervisor=account).count()
		monthly_visits = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
		previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month, supervisor=account).count()
		field_assistants = UserProfile.objects.filter(usertype="Field Assistant")

	elif account_profile.usertype == "Coordinator":
		recently_visited = Visit.objects.filter(supervisor=account).order_by('-date_recorded')
		total_visits = Visit.objects.filter(supervisor=account).count()
		current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month, supervisor=account).count()
		monthly_visits = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
		previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month, supervisor=account).count()
		field_assistants = UserProfile.objects.filter(usertype="Field Assistant", psk_region=account_profile.psk_region)
	elif account_profile.usertype == "Admin":
		recently_visited = Visit.objects.all().order_by('-date_recorded')
		total_visits = Visit.objects.count()
		current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month).count()
		monthly_visits = Visit.objects.filter(visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
		previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month).count()
		field_assistants = UserProfile.objects.filter(usertype="Field Assistant")


	mwezi_huu = calendar.month_name[int(this_month)]
	mwezi_uliopita = calendar.month_name[int(last_month)]
	coordinators = UserProfile.objects.filter(usertype="Coordinator")

	less_ten = Visit.objects.filter(months_of_stock__range=(0, 10)).count()
	less_thirty = Visit.objects.filter(months_of_stock__range=(10, 30)).count()
	less_sixty = Visit.objects.filter(months_of_stock__range=(30, 60)).count()
	less_hundred = Visit.objects.filter(months_of_stock__range=(60, 100)).count()
	try:
	    page = request.GET.get('page', 1)
	except:
	    page = 1

	paginator = Paginator(recently_visited, 50)

	try:
	    recently_visited = paginator.page(page)
	except PageNotAnInteger:
	    recently_visited = paginator.page(1)
	except EmptyPage:
	    recently_visited = paginator.page(paginator.num_pages)

	index = recently_visited.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]

	context = {
		'coordinators' : coordinators,
		'current_month' : current_month,
		'field_assistants' : field_assistants,
		'miaka' : miaka,
		'months_choices' : months_choices,
		'monthly_visits' : monthly_visits,
		'mwezi_huu' : mwezi_huu,
		'mwezi_uliopita' : mwezi_uliopita,
		'previous_month' : previous_month,
		'recently_visited' : recently_visited,
		'total_visits' : total_visits,
		'page_range' : page_range,
		'less_ten' : less_ten,
		'less_thirty' : less_thirty,
		'less_sixty' : less_sixty,
		'less_hundred' : less_hundred

	}
	template = "visits/list-view.html"
	return render(request, template, context)

@login_required(login_url='login')
def visit_details(request, visit_id):
	visit = get_object_or_404(Visit, pk=visit_id)
	template = "visits/visit-details.html"
	context = {
		'visit' : visit
	}

	return render(request, template, context)

@login_required(login_url='login')
def risk_assessment(request):
	less_ten = Visit.objects.filter(months_of_stock__range=(0, 10)).count()
	less_thirty = Visit.objects.filter(months_of_stock__range=(10, 30)).count()
	less_sixty = Visit.objects.filter(months_of_stock__range=(30, 60)).count()
	less_hundred = Visit.objects.filter(months_of_stock__range=(60, 100)).count()
	than_hundred = Visit.objects.filter(months_of_stock > 100).count()



@login_required(login_url='login')
def coordinators_aggregate_visits(request):
	profiles = User.objects.all()
	visits = User.objects.annotate(total_visits=Count('visit__id')).order_by('-total_visits')

	today = datetime.datetime.now()
	this_mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(this_mwaka, i, 1).strftime('%B')))

	template = "visits/coordinators-aggregate.html"
	context = {
		'months_choices' : months_choices,
		'profiles' : profiles,
		'visits' : visits
	}

	return render(request, template, context)

@login_required(login_url='login')
def monthly_coordinators_aggregate_visits(request, mwezi):
	today = datetime.datetime.now()
	this_mwaka = today.year

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(this_mwaka, i, 1).strftime('%B')))
	query_month = calendar.month_name[int(mwezi)]

	profiles = User.objects.all()
	visits = User.objects.filter(visit__visit_date__year=this_mwaka, visit__visit_date__month=mwezi).annotate(total_visits=Count('visit__id')).order_by('-total_visits')
	template = "visits/coordinators-aggregate.html"
	context = {
		'months_choices' : months_choices,
		'profiles' : profiles,
		'query_month' : query_month,
		'visits' : visits
	}

	return render(request, template, context)

# Filter visits by coordinator
@login_required(login_url='login')
def coordinator_visits(request, coordinator_pk):
	account = get_object_or_404(User, pk=coordinator_pk)
	account_profile = get_object_or_404(UserProfile, user=account)

	today = datetime.datetime.now()
	this_mwaka = today.year
	this_month = today.month
	last_month = today.month - 1

	recently_visited = Visit.objects.filter(supervisor=account).order_by('-date_recorded')
	total_visits = Visit.objects.filter(supervisor=account).count()
	monthly_visits = Visit.objects.filter(supervisor=account, visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
	current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month, supervisor=account).count()
	previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month, supervisor=account).count()
	coordinators = UserProfile.objects.filter(usertype="Coordinator")
	field_assistants = UserProfile.objects.filter(usertype="Field Assistant")
	mwezi_huu = calendar.month_name[int(this_month)]
	mwezi_uliopita = calendar.month_name[int(last_month)]

	context = {
		'coordinators' : coordinators,
		'current_month' : current_month,
		'field_assistants' : field_assistants,
		'monthly_visits' : monthly_visits,
		'mwezi_huu' : mwezi_huu,
		'mwezi_uliopita' : mwezi_uliopita,
		'previous_month' : previous_month,
		'recently_visited' : recently_visited,
		'total_visits' : total_visits,
		'account' : account
	}
	template = "visits/index.html"
	return render(request, template, context)

# Filter visits by month
@login_required(login_url='login')
def month_visits(request, mwezi):
	today = datetime.datetime.now()
	this_mwaka = today.year
	this_month = today.month
	last_month = today.month - 1

	miaka = range(2018, this_mwaka+1)
	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(this_mwaka, i, 1).strftime('%B')))

	recently_visited = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=mwezi).order_by('-visit_date')
	total_visits = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=mwezi).count()
	current_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=this_month).count()
	previous_month = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=last_month).count()
	monthly_visits = Visit.objects.filter(visit_date__year=this_mwaka).annotate(month=TruncMonth('visit_date')).values('month').annotate(visits_sum=Count('id'))
	risk_status = Visit.objects.filter(visit_date__year=this_mwaka, visit_date__month=mwezi).values('risk_level').annotate(status_count=Count('id'))
	coordinators = UserProfile.objects.filter(usertype="Coordinator")
	field_assistants = UserProfile.objects.filter(usertype="Field Assistant")

	query_month = calendar.month_abbr[int(mwezi)]
	mwezi_huu = calendar.month_abbr[int(this_month)]
	mwezi_uliopita = calendar.month_abbr[int(last_month)]

	try:
	    page = request.GET.get('page', 1)
	except:
	    page = 1

	paginator = Paginator(recently_visited, 30)

	try:
	    recently_visited = paginator.page(page)
	except PageNotAnInteger:
	    recently_visited = paginator.page(1)
	except EmptyPage:
	    recently_visited = paginator.page(paginator.num_pages)

	index = recently_visited.number - 1
	max_index = len(paginator.page_range)
	start_index = index - 5 if index >= 5 else 0
	end_index = index + 5 if index <= max_index - 5 else max_index
	page_range = paginator.page_range[start_index:end_index]


	context = {
		'coordinators' : coordinators,
		'current_month' : current_month,
		'field_assistants' : field_assistants,
		'miaka' : miaka,
		'months_choices' : months_choices,
		'monthly_visits' : monthly_visits,
		'mwezi_huu' : mwezi_huu,
		'mwezi_uliopita' : mwezi_uliopita,
		'page_range' : page_range,
		'previous_month' : previous_month,
		'query_month' : query_month,
		'risk_status' : risk_status,
		'recently_visited' : recently_visited,
		'this_mwaka' : this_mwaka,
		'total_visits' : total_visits
	}
	template = "visits/index.html"
	return render(request, template, context)



@login_required(login_url='login')
def annual_visits_summary(request):
	today = datetime.datetime.now()
	this_mwaka = today.year
	this_month = today.month
	last_month = today.month - 1

	this_month_v = Visit.objects.filter(visit_date__month=this_month, visit_date__year=this_mwaka).count()
	if last_month < 1:
		last_month_v = Visit.objects.filter(visit_date__month=last_month, visit_date__year=(this_mwaka-1)).count()
	else:
		last_month_v = Visit.objects.filter(visit_date__month=last_month, visit_date__year=this_mwaka).count()
	this_mwaka_v = Visit.objects.filter(visit_date__year=this_mwaka).count()


# Get Average Monthly Consumption
def get_amc(facility):
	hosi = get_object_or_404(Facilities, pk=facility)
	total_nets = Distribution_report.objects.filter(facility=hosi).order_by('-id')[:7]
	totalnets = 0
	for net in total_nets:
		totalnets = totalnets+net.total_nets

	if total_nets.count() > 5:
		amc = int(totalnets)/6
	elif total_nets.count() < 1:
		amc = 1
	else:
		amc = int(totalnets/total_nets.count())
	return amc

# Calculate balance variance
def get_balance_variance(book_bal, physical_count):
	thresh = int(book_bal) - 10
	if int(physical_count) <= thresh:
		return True
	else:
		return False


# Set average monthly consumption on visit details that already exist
# as well as setting the months of stock
def set_amc(request):
	visits = Visit.objects.all()
	for visit in visits:
		hosi = get_object_or_404(Facilities, pk=visit.facility.pk)
		total_nets = Distribution_report.objects.filter(facility=hosi).order_by('-id')[:7]
		totalnets = 0
		for net in total_nets:
			totalnets = totalnets+net.total_nets

		if total_nets.count() > 5:
			amc = int(totalnets/6)
			visit.amc = amc

			if visit.amc < 1:
				stock_status = float(visit.physical_count/1)
			else:
				stock_status = float(visit.physical_count/visit.amc)
			visit.months_of_stock = stock_status
			visit.save()

		elif total_nets.count() < 1:
			amc = 1
			visit.amc = amc
			if visit.amc < 1:
				stock_status = float(visit.physical_count/1)
			else:
				stock_status = float(visit.physical_count/visit.amc)
			visit.months_of_stock = stock_status
			visit.save()
		else:
			amc = int(totalnets/total_nets.count())
			visit.amc = amc

			if visit.amc < 1:
				stock_status = float(visit.physical_count/1)
			else:
				stock_status = float(visit.physical_count/visit.amc)
			visit.months_of_stock = stock_status
			visit.save()

	return redirect('visits:visits_index')

# Update risk status for all the visits if the data had already been populated.
def update_risk_level(request):
	visits = Visit.objects.all()
	for visit in visits:
		if(visit.balance_variance > 10 or visit.balance_variance < -10) or (visit.balance_variance < 0 and visit.balance_variance < visit.amc):
			risk = "High"
			visit.risk_level = risk
			visit.save()
		elif((5 < visit.balance_variance < 10) or (-5 > visit.balance_variance > -10)) or (1 < visit.months_of_stock < 3):
			risk = "Medium"
			visit.risk_level = risk
			visit.save()
		else:
			risk = "Low"
			visit.risk_level = risk
			visit.save()

	return redirect('visits:visits_index')

# Set risk status
def set_risk_status(amc, variance, stock_status):
	if(variance > 10 or variance < -10) or (variance < 0 and variance < amc):
		return "High"
	elif((5 < variance < 10) or (-5 > variance > -10)) or (1 < stock_status < 3):
		return "Medium"
	else:
		return "Low"

#Fetch cordinators email address
def coordinator_email(account):
	coordinator = get_object_or_404(UserProfile, user=account)
	email = User.objects.filter(pk=coordinator.user.pk).values('email')
	data = []

	for i in email:
	    data.append(i)
	return data[0]['email']



@login_required(login_url='login')
def email_sender(request):
	subject = 'Facility visit variance'
	name = "Net Distribution"
	emailFrom = settings.EMAIL_HOST_USER
	message = 'A variance was detected during the visit to this facility'
	emailTo = ['mugunapiero@gmail.com']
	send_mail(subject, message, emailFrom, emailTo, fail_silently=False)

	messages.success(request, "Success! Email sent successfully")
	return redirect('facilities:facilities')

@login_required(login_url='login')
def download_visits_excel(request):
	if request.method == "POST":
		mwezi = request.POST['mwezi']
		mwaka = request.POST['mwaka']

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="visits.csv"'

		writer = csv.writer(response)
		writer.writerow(['supervisor','facility', 'visit_date', 'reporting_frequency', 'quarter_order', 'challenge_solver',
			'ojt_perfomed',
			'policy_compliance',
			'non_compliance_reason',
			'new_anc_moh711',
			'nets_anc_moh711',
		  	'nets_anc_fnprc',
			'nets_anc_variance',
			'new_cwc_moh710',
			'nets_cwc_moh711',
			'nets_cwc_fnprc',
			'nets_cwc_variance',
			'book_bal',
			'physical_count',
			'balance_variance',
			'bal_variance_reason',
			'ld_quantity',
			'ld_invoice_no',
			'ld_date',
			'lld_quantity',
			'lld_invoice_no',
			'lld_date',
			'amc',
			'months_of_stock',
		    'confirmable_cwc',
			'confirmable_anc',
			'store_type',
			'stock_control_card',
			'store_access',
			'pests_risk',
			'fire_prevention',
			'fire_prevention_mechanism',
			'other_remarks',
			'risk_level'])

		visits = Visit.objects.filter(visit_date__month=mwezi, visit_date__year=mwaka).values_list('supervisor','facility', 'visit_date', 'reporting_frequency', 'quarter_order', 'challenge_solver',
			'ojt_perfomed',
			'policy_compliance',
			'non_compliance_reason',
			'new_anc_moh711',
			'nets_anc_moh711',
		  	'nets_anc_fnprc',
			'nets_anc_variance',
			'new_cwc_moh710',
			'nets_cwc_moh711',
			'nets_cwc_fnprc',
			'nets_cwc_variance',
			'book_bal',
			'physical_count',
			'balance_variance',
			'bal_variance_reason',
			'ld_quantity',
			'ld_invoice_no',
			'ld_date',
			'lld_quantity',
			'lld_invoice_no',
			'lld_date',
			'amc',
			'months_of_stock',
		    'confirmable_cwc',
			'confirmable_anc',
			'store_type',
			'stock_control_card',
			'store_access',
			'pests_risk',
			'fire_prevention',
			'fire_prevention_mechanism',
			'other_remarks',
			'risk_level')
		for visit in visits:
		    writer.writerow(visit)

		return response


# Add facilities by excel
@login_required(login_url='login')
def visits_excel_upload(request):
	if request.method == 'POST' and request.FILES['excel_file']:
		myfile = request.FILES['excel_file']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
		for record in records:
			facility = get_object_or_404(Facilities, mfl_code=record['facility'])
			print(facility)
			# supervisor = get_object_or_404(User, pk=record['supervisor'])
			# facility = get_object_or_404(Facilities, mfl_code=record['facility'])
			# visit_date = record['visit_date']
			# reporting_frequency = record['reporting_frequency']
			# quarter_order = record['quarter_order']
			# challenge_solver = record['challenge_solver']
			# ojt_perfomed = record['ojt_performed']
			# policy_compliance = record['policy_compliance']
			# non_compliance_reason = record['non_compliance_reason']
			# new_anc_moh711 = int(record['new_anc_moh711'])
			# nets_anc_moh711 = int(record['nets_anc_moh711'])
			# nets_anc_fnprc = record['nets_anc_fnprc']
			# nets_anc_variance = int(new_anc_moh711 - nets_anc_moh711)
			# new_cwc_moh710 = int(record['new_cwc_moh710'])
			# nets_cwc_moh711 = int(record['nets_cwc_moh711'])
			# nets_cwc_fnprc = int(record['nets_cwc_fnprc'])
			# nets_cwc_variance = int(new_cwc_moh710 - nets_cwc_moh711)
			# book_bal = int(record['book_bal'])
			# physical_count = int(record['physical_count'])
			# balance_variance = int(book_bal - physical_count)
			# bal_variance_reason = record['bal_variance_reason']
			# if record['ld_quantity']:
			# 	ld_quantity = record['ld_quantity']
			# else:
			# 	ld_quantity = 0
			#
			# ld_invoice_no = record['ld_invoice_no']
			# # Blank date fields capture
			# if record['ld_date']:
			# 	ld_date = record['ld_date']
			# else:
			# 	ld_date = datetime.date.today()
			#
			# # Blank quantity fields capture
			# if record['lld_quantity']:
			# 	lld_quantity = record['lld_quantity']
			# else:
			# 	lld_quantity = 0
			# lld_invoice_no = record['lld_invoice_no']
			#
			# # Blank date fields capture
			# if record['lld_date']:
			# 	lld_date = record['lld_date']
			# else:
			# 	lld_date = datetime.date.today()
			# # Average monthly consumption
			# amc = float(get_amc(facility.pk))
			# months_of_stock = float(physical_count/amc)
			# confirmable_cwc = record['confirmable_cwc']
			# confirmable_anc = rrecord['confirmable_anc']
			# store_type = record['store_type']
			# stock_control_card = int(record['stock_control_card'])
			# store_access = record['store_access']
			# pests_risk = record['pests_risk']
			# fire_prevention = record['fire_prevention']
			# fire_prevention_mechanism = record['fire_prevention_mechanism']
			# other_remarks = rrecord['other_remarks']
			# risk_level = set_risk_status(amc, balance_variance, months_of_stock)
			#
			# new_visit = Visit(
			# 		supervisor = supervisor,
			# 		facility = facility,
			# 		visit_date = visit_date,
			# 		reporting_frequency = reporting_frequency,
			# 		quarter_order = quarter_order,
			# 		challenge_solver = challenge_solver,
			# 		ojt_perfomed = ojt_perfomed,
			# 		policy_compliance = policy_compliance,
			# 		non_compliance_reason = non_compliance_reason,
			# 		new_anc_moh711 = new_anc_moh711,
			# 		nets_anc_moh711 = nets_anc_moh711,
			# 		nets_anc_fnprc = nets_anc_fnprc,
			# 		nets_anc_variance = nets_anc_variance,
			# 		new_cwc_moh710 = new_cwc_moh710,
			# 		nets_cwc_moh711 = nets_cwc_moh711,
			# 		nets_cwc_fnprc = nets_cwc_fnprc,
			# 		nets_cwc_variance = nets_cwc_variance,
			# 		book_bal = book_bal,
			# 		physical_count = physical_count,
			# 		balance_variance = balance_variance,
			# 		bal_variance_reason = bal_variance_reason,
			# 		ld_quantity = ld_quantity,
			# 		ld_invoice_no = ld_invoice_no,
			# 		ld_date = ld_date,
			# 		lld_quantity = lld_quantity,
			# 		lld_invoice_no = lld_invoice_no,
			# 		lld_date = lld_date,
			# 		amc = amc,
			# 		months_of_stock = months_of_stock,
			# 		confirmable_cwc = confirmable_cwc,
			# 		confirmable_anc = confirmable_anc,
			# 		store_type = store_type,
			# 		stock_control_card = stock_control_card,
			# 		store_access = store_access,
			# 		pests_risk = pests_risk,
			# 		fire_prevention = fire_prevention,
			# 		fire_prevention_mechanism = fire_prevention_mechanism,
			# 		other_remarks = other_remarks,
			# 		risk_level = risk_level
			# 	).save()
			#
			# if get_balance_variance(book_bal,physical_count):
			# 	region = facility.psk_region
			# 	variance = int(physical_count) - int(book_bal)
			# 	subject = 'Facility visit variance'
			# 	name = "Net Distribution"
			# 	emailFrom = settings.EMAIL_HOST_USER
			# 	message = 'A variance of {} was detected during the visit to facility {}. Kindly check on the same.'.format(variance, facility.facility_name)
			# 	emailTo = ['mugunapiero@gmail.com',coordinator_email(account)]
			#
			# 	send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
	messages.success(request, "Success! Visit details successfully recorded.")
	return redirect("visits:visits_index")






@login_required(login_url='login')
def record_visit(request):
	account = request.user
	if request.method == "POST":
			supervisor = account
			try:
				facility = get_object_or_404(Facilities, mfl_code=request.POST['facility'])
				visit_date = request.POST['visit_date']
				reporting_frequency = request.POST['reporting_frequency']
				quarter_order = request.POST['quarter_order']
				challenge_solver = request.POST['challenge_solver']
				ojt_perfomed = request.POST['ojt_performed']
				policy_compliance = request.POST['policy_compliance']
				non_compliance_reason = request.POST['non_compliance_reason']
				new_anc_moh711 = int(request.POST['new_anc_moh711'])
				nets_anc_moh711 = int(request.POST['nets_anc_moh711'])
				nets_anc_fnprc = request.POST['nets_anc_fnprc']
				nets_anc_variance = int(new_anc_moh711 - nets_anc_moh711)
				new_cwc_moh710 = int(request.POST['new_cwc_moh710'])
				nets_cwc_moh711 = int(request.POST['nets_cwc_moh711'])
				nets_cwc_fnprc = int(request.POST['nets_cwc_fnprc'])
				nets_cwc_variance = int(new_cwc_moh710 - nets_cwc_moh711)
				book_bal = int(request.POST['book_bal'])
				physical_count = int(request.POST['physical_count'])
				balance_variance = int(book_bal - physical_count)
				bal_variance_reason = request.POST['bal_variance_reason']
				if request.POST['ld_quantity']:
					ld_quantity = request.POST['ld_quantity']
				else:
					ld_quantity = 0

				ld_invoice_no = request.POST['ld_invoice_no']
				# Blank date fields capture
				if request.POST['ld_date']:
					ld_date = request.POST['ld_date']
				else:
					ld_date = datetime.date.today()

				# Blank quantity fields capture
				if request.POST['lld_quantity']:
					lld_quantity = request.POST['lld_quantity']
				else:
					lld_quantity = 0
				lld_invoice_no = request.POST['lld_invoice_no']

				# Blank date fields capture
				if request.POST['lld_date']:
					lld_date = request.POST['lld_date']
				else:
					lld_date = datetime.date.today()
				# Average monthly consumption
				amc = float(get_amc(facility.pk))
				months_of_stock = float(physical_count/amc)
				confirmable_cwc = request.POST['confirmable_cwc']
				confirmable_anc = request.POST['confirmable_anc']
				store_type = request.POST['store_type']
				stock_control_card = int(request.POST['stock_control_card'])
				store_access = request.POST['store_access']
				pests_risk = request.POST['pests_risk']
				fire_prevention = request.POST['fire_prevention']
				fire_prevention_mechanism = request.POST['fire_prevention_mechanism']
				other_remarks = request.POST['other_remarks']
				risk_level = set_risk_status(amc, balance_variance, months_of_stock)

			except:
				messages.error(request, "Error! Facility {} details were not added. Check all required fields are not blank.".format(request.POST['facility']))
				return render(request, "visits/record-visit.html")


			if Visit.objects.filter(facility=facility).filter(visit_date=visit_date).exists():
				messages.error(request, "Error! Facility: {} visit details you are entering appear to be duplicate. Kindly confirm.".format(facility.facility_name))
				return redirect("visits:record_visit")
			else:
				new_visit = Visit(
						supervisor = supervisor,
						facility = facility,
						visit_date = visit_date,
						reporting_frequency = reporting_frequency,
						quarter_order = quarter_order,
						challenge_solver = challenge_solver,
						ojt_perfomed = ojt_perfomed,
						policy_compliance = policy_compliance,
						non_compliance_reason = non_compliance_reason,
						new_anc_moh711 = new_anc_moh711,
						nets_anc_moh711 = nets_anc_moh711,
						nets_anc_fnprc = nets_anc_fnprc,
						nets_anc_variance = nets_anc_variance,
						new_cwc_moh710 = new_cwc_moh710,
						nets_cwc_moh711 = nets_cwc_moh711,
						nets_cwc_fnprc = nets_cwc_fnprc,
						nets_cwc_variance = nets_cwc_variance,
						book_bal = book_bal,
						physical_count = physical_count,
						balance_variance = balance_variance,
						bal_variance_reason = bal_variance_reason,
						ld_quantity = ld_quantity,
						ld_invoice_no = ld_invoice_no,
						ld_date = ld_date,
						lld_quantity = lld_quantity,
						lld_invoice_no = lld_invoice_no,
						lld_date = lld_date,
						amc = amc,
						months_of_stock = months_of_stock,
						confirmable_cwc = confirmable_cwc,
						confirmable_anc = confirmable_anc,
						store_type = store_type,
						stock_control_card = stock_control_card,
						store_access = store_access,
						pests_risk = pests_risk,
						fire_prevention = fire_prevention,
						fire_prevention_mechanism = fire_prevention_mechanism,
						other_remarks = other_remarks,
						risk_level = risk_level
					).save()

				if get_balance_variance(book_bal,physical_count):
					region = facility.psk_region
					variance = int(physical_count) - int(book_bal)
					subject = 'Facility visit variance'
					name = "Net Distribution"
					emailFrom = settings.EMAIL_HOST_USER
					message = 'A variance of {} was detected during the visit to facility {}. Kindly check on the same.'.format(variance, facility.facility_name)
					emailTo = ['mugunapiero@gmail.com',coordinator_email(account)]

					send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
				messages.success(request, "Success! Visit details for {} successfully recorded.".format(facility.facility_name))
				return redirect("visits:visits_index")


	else:
		form = NewVisitForm()
		context = {
			'form' : form
		}
		template = "visits/record-visit.html"
		return render(request, template, context)

# Get duplicate values for a specific period
@login_required(login_url='authentication:login')
def get_duplicate_visits(request):
	today = datetime.datetime.now()
	if request.method == "POST":
		mwezi = int(request.POST['mwezi'])
		mwaka = int(request.POST['mwaka'])

		duplicates = Visit.objects.values('facility__mfl_code', 'facility__facility_name').annotate(visit_count=Count('id')).filter(visit_count__gt=1, visit_date__year=mwaka, visit_date__month=mwezi)

	months_choices = []
	for i in range(1,13):
	    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))
	miaka = range(2018, today.year+1)
	query_month = calendar.month_name[mwezi]

	context = {
		'duplicates' : duplicates,
		'miaka' : miaka,
		'months_choices' : months_choices,
		'query_month' : query_month
	}
	template = "visits/duplicate_visits.html"
	return render(request, template, context)

@login_required(login_url='authentication:login')
def fetch_visits_by_risk_level(request):
	leo = datetime.datetime.now()
	this_mwaka = leo.year
	account = request.user
	if request.method == "POST":
		mwezi = int(request.POST['mwezi'])
		mwaka = int(request.POST['mwaka'])
		risk = request.POST['risk']

		visits = Visit.objects.filter(visit_date__month=mwezi, visit_date__year=mwaka, risk_level=risk)
		months_choices = []
		for i in range(1,13):
		    months_choices.append((i, datetime.date(mwaka, i, 1).strftime('%B')))
		miaka = range(2018, int(this_mwaka+1))
		mwezi = calendar.month_name[mwezi]

		context = {
			'miaka' : miaka,
			'mwaka' : mwaka,
			'mwezi' : mwezi,
			'months_choices' : months_choices,
			'risk' : risk,
			'visits' : visits
		}
		template = "visits/risk_filter.html"
		return render(request, template, context)

















# def last_six_months(facility):
# 	hosi = get_object_or_404(Facilities, pk=facility)
# 	total_nets = Distribution_report.objects.filter(facility=hosi).order_by('-id')[:7]
# 	totalnets = 0
# 	for net in total_nets:
# 		totalnets = totalnets+net.total_nets


# 	return totalnets
