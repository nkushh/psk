from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pyexcel as pe
import json
from .models import Profile, Facilities
from distribution.models import Nets_distributed, Distribution_report
from visits.models import Visit

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    total_facilities = Facilities.objects.all().count()
    accounts = User.objects.count()
    nets_distributed = Nets_distributed.objects.aggregate(distributed_nets=Sum('nets_issued'))
    nets_issued = Distribution_report.objects.aggregate(issued_nets=Sum('total_nets'))
    facilities_by_county = Facilities.objects.values('county').annotate(county_facilities=Count('county')).order_by('-county_facilities')
    context = {
        'accounts' : accounts,
        'nets_distributed' : nets_distributed,
        'nets_issued' : nets_issued,
        'total_facilities' : total_facilities,
        'facilities_by_county' : facilities_by_county
        }

    template = "facilities/index.html"
    return render(request, template, context)

@login_required(login_url='login')
def facilities(request):
	context = {
		'facilities' : Facilities.objects.all()[:50],
	}
	template = "facilities/facilities.html"
	return render(request, template, context)

@login_required(login_url='login')
def new_facility(request):
	context = {}
	template = "facilities/add-facility.html"
	return render(request, template, context)

@login_required(login_url='login')
def facility_details(request, facility_pk):
    facility = get_object_or_404(Facilities, pk=facility_pk)
    nets_delivered = Nets_distributed.objects.filter(facility=facility).order_by('-date_issued')
    nets_issued = Distribution_report.objects.filter(facility=facility).order_by('id')
    visits = Visit.objects.filter(facility=facility).order_by('-visit_date')

    context = {
        'facility' : facility,
        'nets_delivered' : nets_delivered,
        'nets_issued' : nets_issued,
        'visits' : visits
    }

    template = "facilities/facility-details.html"
    return render(request, template, context)

@login_required(login_url='login')
def excel_uploaddd(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        myfile = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
        for record in records:
        	name = record['Name']
        	sex = record['sex']
        	age = record['age']

        	Profile(name=name, sex=sex,age=age).save()
        return redirect('facilities:add_facility')
    else:
    	return redirect('facilities:facilities')

@login_required(login_url='login')
def excel_upload(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        myfile = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
        for record in records:
        	mfl_code = record['MFL Code']
        	facility_name = record['Health Facility']
        	county = record['County']
        	sub_county = record['Sub County']
        	facility_ownership = record['Facility Ownership']
        	epidemiological_zone = record['Epidemiological Zone']

        	Facilities(
        			mfl_code=mfl_code, 
        			facility_name=facility_name,
        			county=county, 
        			sub_county=sub_county, 
        			facility_ownership=facility_ownership, 
        			epidemiological_zone=epidemiological_zone
        			).save()
        return redirect('facilities:add_facility')
    else:
    	return redirect('facilities:facilities')

# Facilities Autocomplete live search
@login_required(login_url='login')
def facilities_autocomplete(request,*args,**kwargs):
    data = request.GET
    facility = data.get("term")
    if facility:
        facilities = Facilities.objects.filter(facility_name__startswith = facility)
        results = []
        for hosi in facilities:
            hosi_json = {}
            hosi_json['id'] = hosi.id
            hosi_json['label'] = hosi.facility_name
            hosi_json['value'] = hosi.facility_name
            results.append(hosi_json)
        data = json.dumps(results)
    else:
        facilities = Facilities.objects.all()
        results = []
        for hosi in facilities:
            hosi_json = {}
            hosi_json['id'] = hosi.id
            hosi_json['label'] = hosi.facility_name
            hosi_json['value'] = hosi.facility_name
            results.append(hosi_json)
        data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required(login_url='login')
def facility_search(request):
    if request.method=="GET":
        search_query = request.GET.get('facility')
        facilities = Facilities.objects.filter(Q(facility_name__istartswith=search_query) | Q(mfl_code__istartswith=search_query))
    context = {
        'facilities' : facilities
    }
    template = "facilities/facilities.html"
    return render(request, template, context)


