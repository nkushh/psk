from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from facilities.models import Facilities
from distribution.models import Distribution_report
from .models import Visit

# Create your views here.
@login_required(login_url='login')
def visits_index(request):
	account = request.user
	recently_visited = Visit.objects.all()
	
	context = {
		'recently_visited' : recently_visited
	}
	template = "visits/index.html"
	return render(request, template, context)

def get_amc(facility):
	hosi = get_object_or_404(Facilities, pk=facility)
	total_nets = Distribution_report.objects.filter(facility=hosi).order_by('-id')[:7]
	totalnets = 0
	for net in total_nets:
		totalnets = totalnets+net.total_nets

	amc = int(totalnets)/6
	return amc

# def last_six_months(facility):
# 	hosi = get_object_or_404(Facilities, pk=facility)
# 	total_nets = Distribution_report.objects.filter(facility=hosi).order_by('-id')[:7]
# 	totalnets = 0
# 	for net in total_nets:
# 		totalnets = totalnets+net.total_nets


# 	return totalnets

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
			messages.success(request, "Success! Visit details for {} successfully recorded.".format(facility.facility_name))
			return redirect("visits:record_visit")
	else:
		context = {}
		template = "visits/record-visit.html"
		return render(request, template, context)



@login_required(login_url='login')
def visit_form(request):
	account = request.user

	context = {}
	template = "visits/form-pickers.html"
	return render(request, template, context)
