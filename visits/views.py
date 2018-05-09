from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import UserProfile
from facilities.models import Facilities
from distribution.models import Distribution_report
from .models import Visit
import datetime, calendar

# Create your views here.
@login_required(login_url='login')
def visits_index(request):
	account = request.user
	recently_visited = Visit.objects.all()
	total_visits = Visit.objects.count()
	
	context = {
		'recently_visited' : recently_visited,
		'total_visits' : total_visits,
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

def coordinator_email(region):
	coordinator = get_object_or_404(UserProfile, psk_region=region)
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
def record_visit(request):
	account = request.user
	if request.method == "POST":
			supervisor = account
			facility = get_object_or_404(Facilities, facility_name=request.POST['facility'])
			visit_date = request.POST['visit_date']
			reporting_frequency = request.POST['reporting_frequency']
			quarter_order = request.POST['quarter_order']
			challenge_solver = request.POST['challenge_solver']
			ojt_perfomed = request.POST['ojt_performed']
			policy_compliance = request.POST['policy_compliance']
			non_compliance_reason = request.POST['non_compliance_reason']
			new_anc_moh711 = request.POST['new_anc_moh711']
			nets_anc_moh711 = request.POST['nets_anc_moh711']
			nets_anc_fnprc = request.POST['nets_anc_fnprc']
			nets_anc_variance = int(int(new_anc_moh711) - int(nets_anc_moh711))
			new_cwc_moh710 = request.POST['new_cwc_moh710']
			nets_cwc_moh711 = request.POST['nets_cwc_moh711']
			nets_cwc_fnprc = request.POST['nets_cwc_fnprc']
			nets_cwc_variance = int(int(new_cwc_moh710) - int(nets_cwc_moh711))
			book_bal = request.POST['book_bal']
			physical_count = request.POST['physical_count']
			balance_variance = int(int(book_bal) - int(physical_count))
			bal_variance_reason = request.POST['bal_variance_reason']
			ld_quantity = request.POST['ld_quantity']
			ld_invoice_no = request.POST['ld_invoice_no']
			ld_date = request.POST['ld_date']
			lld_quantity = request.POST['lld_quantity']
			lld_invoice_no = request.POST['lld_invoice_no']
			lld_date = request.POST['lld_date']
			amc = get_amc(facility.pk)
			months_of_stock = float(int(physical_count)/int(amc))
			confirmable_cwc = request.POST['confirmable_cwc']
			confirmable_anc = request.POST['confirmable_anc']
			nets_stored_in = request.POST['nets_stored_in']
			store_type = request.POST['store_type']
			stock_control_card = request.POST['stock_control_card']
			store_access = request.POST['store_access']
			pests_risk = request.POST['pests_risk']
			fire_prevention = request.POST['fire_prevention']
			fire_prevention_mechanism = request.POST['fire_prevention_mechanism']
			other_remarks = request.POST['other_remarks']

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
					nets_stored_in = nets_stored_in,
					store_type = store_type,
					stock_control_card = stock_control_card,
					store_access = store_access,
					pests_risk = pests_risk,
					fire_prevention = fire_prevention,
					fire_prevention_mechanism = fire_prevention_mechanism,
					other_remarks = other_remarks
				).save()

			if book_bal != physical_count:
				region = facility.psk_region
				variance = int(physical_count) - int(book_bal)
				subject = 'Facility visit variance'
				name = "Net Distribution"
				emailFrom = settings.EMAIL_HOST_USER
				message = 'A variance of {} was detected during the visit to facility {}. Kindly check on the same.'.format(variance, facility.facility_name)
				emailTo = ['mugunapiero@gmail.com',coordinator_email(region)]

				send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
			messages.success(request, "Success! Visit details for {} successfully recorded.".format(facility.facility_name))
			return redirect("visits:visits_index")
	else:
		context = {}
		template = "visits/record-visit.html"
		return render(request, template, context)
















# def last_six_months(facility):
# 	hosi = get_object_or_404(Facilities, pk=facility)
# 	total_nets = Distribution_report.objects.filter(facility=hosi).order_by('-id')[:7]
# 	totalnets = 0
# 	for net in total_nets:
# 		totalnets = totalnets+net.total_nets


# 	return totalnets

