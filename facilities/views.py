from authentication.models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Counties, Epidemiological_zones, Facilities, Regions
from distribution.models import Nets_distributed, Distribution_report
from visits.models import Visit
import json, datetime, calendar, csv
import pyexcel as pe


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    account = request.user
    account_profile = get_object_or_404(UserProfile, user=account)
    today = datetime.datetime.now()

    
    accounts = User.objects.count()
    
    nets_issued = Distribution_report.objects.aggregate(issued_nets=Sum('total_nets'))

    if account_profile.usertype != "Admin":
        nets_distributed = Nets_distributed.objects.filter(facility__psk_region=account_profile.psk_region).aggregate(distributed_nets=Sum('nets_issued'))
        total_facilities = Facilities.objects.filter(psk_region=account_profile.psk_region).count()
        total_visits = Visit.objects.filter(supervisor=account).count()
    else:
        nets_distributed = Nets_distributed.objects.aggregate(distributed_nets=Sum('nets_issued'))
        total_facilities = Facilities.objects.count()
        total_visits = Visit.objects.count()
    # nets_to_anc = Distribution_report.objects.filter(dist_month="", dist_year=today.year).aggregate(issued_nets=Sum('anc_nets'))
    # nets_to_cwc = Distribution_report.objects.filter().aggregate(issued_nets=Sum('total_nets'))
    region_distribution = Nets_distributed.objects.values('facility__psk_region').annotate(region_total=Sum('nets_issued')).order_by('-region_total')
    region_visits = Visit.objects.values('facility__psk_region').annotate(visits_total=Count('pk')).order_by('-visits_total')
    facilities_by_county = Facilities.objects.values('county').annotate(county_facilities=Count('county')).order_by('-county_facilities')
    facilities_by_ez = Facilities.objects.values('epidemiological_zone').annotate(ez_facilities=Count('epidemiological_zone')).order_by('-ez_facilities')
    

    context = {
        'accounts' : accounts,
        'facilities_by_ez' : facilities_by_ez,
        'nets_distributed' : nets_distributed,
        'nets_issued' : nets_issued,
        'region_distribution' : region_distribution,
        'region_visits' : region_visits,
        'total_facilities' : total_facilities,
        'total_visits' : total_visits,
        'facilities_by_county' : facilities_by_county
        }

    template = "facilities/index.html"
    return render(request, template, context)

@login_required(login_url='login')
def facilities(request):
    counties = Facilities.objects.values('county').distinct()
    facilities = Facilities.objects.all()
    facility_count = Facilities.objects.all().count()
    page_count = int(facility_count/50)
    try:
        page = request.GET.get('page', 1)
    except:
        page = 1

    paginator = Paginator(facilities, 50)

    try:
        facilities = paginator.page(page)
    except PageNotAnInteger:
        facilities = paginator.page(1)
    except EmptyPage:
        facilities = paginator.page(paginator.num_pages)

    index = facilities.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'counties' : counties,
        'facilities' : facilities,
        'page_count' : page_count,
        'page_range' : page_range
    }
    template = "facilities/facilities.html"
    return render(request, template, context)

# Download them all
@login_required(login_url='login')
def download_facilities_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facilities.csv"'

    writer = csv.writer(response)
    writer.writerow(['Region', 'MFL', 'Name', 'County', 'Sub county'])

    facilities = Facilities.objects.all().values_list('psk_region', 'mfl_code', 'facility_name', 'county', 'sub_county')
    for facility in facilities:
        writer.writerow(facility)

    return response

# Fetch facilities by county
@login_required(login_url='login')
def county_facilities(request, county_name):
    county = county_name
    counties = Facilities.objects.values('county').distinct()
    sub_counties = Facilities.objects.filter(county=county).values('sub_county').distinct()
    facilities = Facilities.objects.filter(county=county).order_by('facility_name')
    facility_count = Facilities.objects.filter(county=county).count()
    page_count = int(facility_count/50)

    page = request.GET.get('page', 1)

    paginator = Paginator(facilities, 50)

    try:
        facilities = paginator.page(page)
    except PageNotAnInteger:
        facilities = paginator.page(1)
    except EmptyPage:
        facilities = paginator.page(paginator.num_pages)

    index = facilities.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'county' : county,
        'counties' : counties,
        'facilities' : facilities,
        'facility_count' : facility_count,
        'page_count' : page_count,
        'page_range' : page_range,
        'sub_counties' : sub_counties
    }
    template = "facilities/facilities.html"
    return render(request, template, context)

@login_required(login_url='login')
def subcounty_facilities(request, county_name, subcounty):
    county = county_name
    counties = Facilities.objects.values('county').distinct()
    sub_counties = Facilities.objects.filter(county=county).values('sub_county').distinct()
    facilities = Facilities.objects.filter(sub_county=subcounty).order_by('facility_name')
    facility_count = Facilities.objects.filter(sub_county=subcounty).count()
    page_count = int(facility_count/50)

    page = request.GET.get('page', 1)

    paginator = Paginator(facilities, 50)

    try:
        facilities = paginator.page(page)
    except PageNotAnInteger:
        facilities = paginator.page(1)
    except EmptyPage:
        facilities = paginator.page(paginator.num_pages)

    index = facilities.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'county' : county_name,
        'counties' : counties,
        'facilities' : facilities,
        'facility_count' : facility_count,
        'page_count' : page_count,
        'page_range' : page_range,
        'sub_counties' : sub_counties
    }
    template = "facilities/facilities.html"
    return render(request, template, context)

def facility_region(county):
    region = Facilities.objects.filter(county=county).values('psk_region').distinct()
    data = []
    for i in region:
        data.append(i)
    return data[0]['psk_region']

def facility_zone(county):
    zone = Facilities.objects.filter(county=county).values('epidemiological_zone').distinct()
    data = []
    for i in zone:
        data.append(i)
    return data[0]['epidemiological_zone']

@login_required(login_url='login')
def new_facility(request):
    if request.method=="POST":
        mfl_code = request.POST['mfl_code']
        facility_name = request.POST['facility_name'].title()
        county = request.POST['county'].title()
        sub_county = request.POST['sub_county'].title()
        constituency = request.POST['constituency'].title()
        ward = request.POST['ward'].title()
        facility_ownership = request.POST['facility_ownership']
        epidemiological_zone = facility_zone(county)
        psk_region = facility_region(county)

        if Facilities.objects.filter(mfl_code=mfl_code).exists():
            messages.error(request, "Error! MFL Code {} already exists. Kindly enter a different one.".format(mfl_code))
            return redirect('facilities:new_facility')
        else:
            Facilities(
                    psk_region = psk_region,
                    mfl_code = mfl_code,
                    facility_name = facility_name,
                    county = county,
                    sub_county = sub_county,
                    constituency = constituency,
                    ward = ward,
                    facility_ownership = facility_ownership,
                    epidemiological_zone = epidemiological_zone
                ).save()
            messages.success(request, "Success! {} addded to facilities database successfully".format(facility_name))
            return redirect('facilities:facilities')
    else:
        counties = Facilities.objects.values('county').distinct()
        regions = Regions.objects.all()
        
        context = {
            'counties' : counties,
            'regions' : regions
        }
        template = "facilities/add-facility.html"
        return render(request, template, context)

@login_required(login_url='login')
def update_facility(request, facility_pk):
    facility = get_object_or_404(Facilities, pk=facility_pk)
    if request.method=="POST":
        psk_region = request.POST['psk_region']
        mfl_code = request.POST['mfl_code']
        facility_name = request.POST['facility_name'].title()
        county = request.POST['county'].title()
        sub_county = request.POST['sub_county'].title()
        constituency = request.POST['constituency'].title()
        ward = request.POST['ward'].title()
        facility_ownership = request.POST['facility_ownership']
        epidemiological_zone = facility_zone(county)

        facility.mfl_code = mfl_code
        facility.facility_name = facility_name
        facility.county = county
        facility.sub_county = sub_county
        facility.constituency = constituency
        facility.ward = ward
        facility.epidemiological_zone = epidemiological_zone
        facility.psk_region = psk_region

        facility.save()
        messages.success(request, "Success! {} details have been updated successfully.".format(facility_name))
        return redirect("facilities:facility_details", facility_pk=facility.pk)


    else:
        counties = Facilities.objects.values('county').distinct()
        regions = Regions.objects.all()
        
        context = {
            'facility' : facility,
            'counties' : counties,
            'regions' : regions
        }
        template = "facilities/update-facility.html"
        return render(request, template, context)

# Add facilities by excel
@login_required(login_url='login')
def facilities_excel_upload(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        myfile = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
        for record in records:
            mfl_code = record['mfl']
            facility_name = record['name'].title()
            county = record['county'].title()
            sub_county = record['subcounty'].title()
            constituency = record['constituency'].title()
            ward = record['ward'].title()
            facility_ownership = record['ownership']
            epidemiological_zone = record['ez']

            if Facilities.objects.filter(mfl_code=mfl_code):
                continue
            else:

                Facilities(
                        mfl_code = mfl_code,
                        facility_name = facility_name,
                        county = county,
                        sub_county = sub_county,
                        constituency = constituency,
                        ward = ward,
                        facility_ownership = facility_ownership,
                        epidemiological_zone = epidemiological_zone
                        ).save()
        messages.success(request, "Success! Facilities added successfully.")        
        return redirect('facilities:facilities')
    else:
        template = "facilities/add-facilities.html"
        return render(request, template)

# Fetch facility details
@login_required(login_url='login')
def facility_details(request, facility_pk):
    facility = get_object_or_404(Facilities, pk=facility_pk)
    nets_delivered = Nets_distributed.objects.filter(facility=facility).order_by('-date_issued')
    nets_issued = Distribution_report.objects.filter(facility=facility).order_by('id')
    visits = Visit.objects.filter(facility=facility).order_by('-visit_date')
    nets_delivered_count = Nets_distributed.objects.filter(facility=facility).aggregate(total_delivered=Sum('nets_issued'))
    nets_issued_count = Distribution_report.objects.filter(facility=facility).aggregate(total_issued=Sum('total_nets'))
    visits_count = Visit.objects.filter(facility=facility).count()

    context = {
        'facility' : facility,
        'nets_delivered' : nets_delivered,
        'nets_delivered_count' : nets_delivered_count,
        'nets_issued' : nets_issued,
        'nets_issued_count' : nets_issued_count,
        'visits' : visits,
        'visits_count' : visits_count
    }

    template = "facilities/facility-details.html"
    return render(request, template, context)



# Facilities Autocomplete live search
@login_required(login_url='login')
def facilities_autocomplete(request,*args,**kwargs):
    data = request.GET
    facility = data.get("term")
    if facility:
        facilities = Facilities.objects.filter(status=1, facility_name__startswith = facility)
        results = []
        for hosi in facilities:
            hosi_json = {}
            hosi_json['id'] = hosi.id
            hosi_json['label'] = hosi.facility_name +" - "+hosi.sub_county
            hosi_json['value'] = hosi.mfl_code
            results.append(hosi_json)
        data = json.dumps(results)
    else:
        facilities = Facilities.objects.all()
        results = []
        for hosi in facilities:
            hosi_json = {}
            hosi_json['id'] = hosi.id
            hosi_json['label'] = hosi.facility_name +" - "+hosi.sub_county
            hosi_json['value'] = hosi.mfl_code
            results.append(hosi_json)
        data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required(login_url='login')
def facility_search(request):
    counties = Facilities.objects.values('county').distinct()
    if request.method=="GET":
        search_query = request.GET.get('facility')
        facilities = Facilities.objects.filter(Q(facility_name__istartswith=search_query) | Q(mfl_code__istartswith=search_query))
    context = {
        'counties' : counties,
        'facilities' : facilities
    }
    template = "facilities/facilities.html"
    return render(request, template, context)

@login_required(login_url='login')
def delete_all_facilities(request):
    facilities = Facilities.objects.all()
    facilities.delete()
    return redirect("facilities:facilities")

@login_required(login_url='login')
def delete_facility(request, facility_pk):
    facility = get_object_or_404(Facilities, pk=facility_pk)
    facility.status = 0
    facility.save()
    messages.success(request, "Success! Facility details deleted.")
    return redirect("facilities:facilities")

@login_required(login_url='login')
def delete_facility_2(request, facility_pk):
    facility = get_object_or_404(Facilities, pk=facility_pk)
    facility.delete()
    messages.success(request, "Success! Facility details deleted.")
    return redirect("facilities:facilities")


# PSK Regions Module.
# CRUD functions for regions
@login_required(login_url='login')
def psk_regions(request):
    regions = Regions.objects.all().order_by('region_name')

    try:
        page = request.GET.get('page', 1)
    except:
        page = 1

    paginator = Paginator(regions, 50)

    try:
        regions = paginator.page(page)
    except PageNotAnInteger:
        regions = paginator.page(1)
    except EmptyPage:
        regions = paginator.page(paginator.num_pages)

    index = regions.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    template = "facilities/regions.html"
    context = {
        'regions' : regions,
        'page_range' : page_range
    }
    return render(request, template, context)

@login_required(login_url='login')
def new_region(request):
    if request.method=="POST":
        region_name = request.POST['region_name'].title()
        if Regions.objects.filter(region_name=region_name).exists():
            messages.error(request, "Error! The {} region already exists".format(region_name))
            return redirect('facilities:psk_regions')
        else:
            Regions(region_name=region_name).save()
            messages.success(request, "Success! {} region has been added successfully".format(region_name))
            return redirect('facilities:psk_regions')
    else:
        template = "facilities/add-region.html"
        context = {}
        return render(request, template, context)

@login_required(login_url='login')
def update_region(request, region_pk):
    region = get_object_or_404(Regions, pk=region_pk)
    if request.method=="POST":
        updated_region_name = request.POST['region_name'].title()
        region.region_name = updated_region_name
        region.save()
        messages.success(request, "Success! {} region has been updated successfully".format(updated_region_name))
        return redirect('facilities:psk_regions')
    else:
        template = "facilities/update-region.html"
        context = {
            'region' : region
        }
        return render(request, template, context)

@login_required(login_url='login')
def delete_region(request, region_pk):
    region = get_object_or_404(Regions, pk=region_pk)
    region_name = region.region_name
    region.delete()
    messages.success(request, "Success! {} region details have been permanently deleted.".format(region_name))
    return redirect('facilities:psk_regions')



# PSK Epidemiological Zones Module.
# CRUD functions for zones
@login_required(login_url='login')
def transmission_zones(request):
    zones = Epidemiological_zones.objects.all().order_by('zone_name')

    try:
        page = request.GET.get('page', 1)
    except:
        page = 1

    paginator = Paginator(zones, 50)

    try:
        zones = paginator.page(page)
    except PageNotAnInteger:
        zones = paginator.page(1)
    except EmptyPage:
        zones = paginator.page(paginator.num_pages)

    index = zones.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    template = "facilities/zones.html"
    context = {
        'zones' : zones,
        'page_range' : page_range
    }
    return render(request, template, context)

@login_required(login_url='login')
def new_zone(request):
    if request.method=="POST":
        zone_name = request.POST['zone_name'].title()
        if Epidemiological_zones.objects.filter(zone_name=zone_name).exists():
            messages.error(request, "Error! The {} epidemiological zone already exists".format(zone_name))
            return redirect('facilities:transmission_zones')
        else:
            Epidemiological_zones(zone_name=zone_name).save()
            messages.success(request, "Success! {} epidemiological zone has been added successfully".format(zone_name))
            return redirect('facilities:transmission_zones')
    else:
        template = "facilities/add-zone.html"
        context = {}
        return render(request, template, context)

@login_required(login_url='login')
def update_zone(request, zone_pk):
    zone = get_object_or_404(Epidemiological_zones, pk=zone_pk)
    if request.method=="POST":
        updated_zone_name = request.POST['zone_name'].title()
        zone.zone_name = updated_zone_name
        zone.save()
        messages.success(request, "Success! {} epidemiological zone has been updated successfully".format(updated_zone_name))
        return redirect('facilities:transmission_zones')
    else:
        template = "facilities/update-zone.html"
        context = {
            'zone' : zone
        }
        return render(request, template, context)

@login_required(login_url='login')
def delete_zone(request, zone_pk):
    zone = get_object_or_404(Epidemiological_zones, pk=zone_pk)
    zone_name = zone.zone_name
    zone.delete()
    messages.success(request, "Success! {} zone details have been permanently deleted.".format(zone_name))
    return redirect('facilities:transmission_zones')


# SUPER FUNCTIONS
@login_required(login_url='login')
def county_name_change(request):
    if request.method=="POST":
        old_county_name = request.POST['old_county_name'].title()
        new_county_name = request.POST['new_county_name'].title()
        facilities = Facilities.objects.filter(county=old_county_name)

        for facility in facilities:
            facility.county = new_county_name
            facility.save()
        messages.success(request, "Success! {} changed to {}".format(old_county_name, new_county_name))
        return redirect('facilities:facilities')
    else:    
        template = "facilities/facilities.html"
        return render(request, template, context)

@login_required(login_url='login')
def region_name_change(request):
    if request.method=="POST":
        old_region_name = request.POST['old_region_name'].title()
        new_region_name = request.POST['new_region_name'].title()
        facilities = Facilities.objects.filter(psk_region=old_region_name)

        for facility in facilities:
            facility.psk_region = new_region_name
            facility.save()
        messages.success(request, "Success! {} changed to {}".format(old_region_name, new_region_name))
        return redirect('facilities:facilities')
    else:    
        template = "facilities/facilities.html"
        return render(request, template, context)

@login_required(login_url='login')
def facility_settings(request):
    template = "facilities/facility-settings.html"
    regions = Regions.objects.all()
    context = {
        'regions' : regions
    }
    return render(request, template, context)

@login_required(login_url='login')
def set_facility_region(request, psk_region):
    if psk_region:
        region = psk_region
        if region=="Central":
            facilities = Facilities.objects.filter(Q(county="Kiambu") | Q(county="Murang'a") | Q(county="Kitui"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()
        elif region=="Central Nyanza":
            facilities = Facilities.objects.filter(Q(county="Kisumu") | Q(county="Siaya") | Q(county="Homa Bay"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()
        elif region=="Coast":
            facilities = Facilities.objects.filter(Q(county="Mombasa") | Q(county="Kwale") | Q(county="Kilifi") | Q(county="Lamu") | Q(county="Tana River") | Q(county="Taita Taveta"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()
        elif region=="Mountain":
            facilities = Facilities.objects.filter(Q(county="Meru") | Q(county="Embu") | Q(county="Kirinyaga") | Q(county="Isiolo") | Q(county="Tharaka Nithi"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()

        elif region=="Nairobi 2":
            facilities = Facilities.objects.filter(Q(county="Kajiado") | Q(county="Makueni") | Q(county="Machakos"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()

        elif region=="North Rift":
            facilities = Facilities.objects.filter(Q(county="Baringo") | Q(county="West Pokot") | Q(county="Uasin Gishu") | Q(county="Trans Nzoia") | Q(county="Elgeyo Marakwet"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()

        elif region=="South Nyanza":
            facilities = Facilities.objects.filter(Q(county="Migori") | Q(county="Kisii") | Q(county="Nyamira"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()

        elif region=="South Rift":
            facilities = Facilities.objects.filter(Q(county="Kericho") | Q(county="Nandi") | Q(county="Bomet") | Q(county="Narok"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()

        elif region=="Western":
            facilities = Facilities.objects.filter(Q(county="Busia") | Q(county="Vihiga") | Q(county="Bungoma") | Q(county="Kakamega"))
            for facility in facilities:
                facility.psk_region = region
                facility.save()
        else:
            messages.warning(request, "Warning! The provided region is not valid. Kindly enter a valid PS Kenya region")
            return redirect('facilities:facilities')

        messages.success(request, "Success! {} region set to {} facilities".format(region, facilities.count()))
        return redirect('facilities:facility_settings')

    else:
            template = "facilities/facility-settings.html"
            return render(request, template)

@login_required(login_url='login')
def set_facility_zone(request, psk_zone):
    if psk_zone:
        if zone=="Seasonal Transmission":
            facilities = Facilities.objects.filter(Q(county="Kajiado") | Q(county="Makueni") | Q(county="Kitui") | Q(county="Machakos") | Q(county="Kimabu") | Q(county="Murang'a") | Q(county="Kirinyaga") | Q(county="Embu") | Q(county="Tharaka Nithi") | Q(county="Meru") | Q(county="Isiolo"))
            for facility in facilities:
                facility.epidemiological_zone = zone
                facility.save()
        elif region=="Highland Epidemic":
            facilities = Facilities.objects.filter(Q(county="Narok") | Q(county="Kisii") | Q(county="Bomet") | Q(county="Nyamira") | Q(county="Kericho") | Q(county="Nandi") | Q(county="Uasin Gishu") | Q(county="Baringo") | Q(county="Elgeyo Marakwet") | Q(county="Trans Nzoia") | Q(county="West Pokot"))
            for facility in facilities:
                facility.epidemiological_zone = zone
                facility.save()
        elif region=="Coast Endemic":
            facilities = Facilities.objects.filter(Q(county="Mombasa") | Q(county="Kwale") | Q(county="Kilifi") | Q(county="Lamu") | Q(county="Tana River") | Q(county="Taita Taveta"))
            for facility in facilities:
                facility.epidemiological_zone = zone
                facility.save()
        elif region=="Lake Endemic":
            facilities = Facilities.objects.filter(Q(county="Migori") | Q(county="Homa Bay") | Q(county="Kisumu") | Q(county="Vihiga") | Q(county="Siaya") | Q(county="Kakamega") | Q(county="Busia") | Q(county="Bungoma"))
            for facility in facilities:
                facility.epidemiological_zone = zone
                facility.save()
        else:
            messages.warning(request, "Warning! The provided region is not valid. Kindly enter a valid PS Kenya region")
            return redirect('facilities:facilities')

        messages.success(request, "Success! {} region set to {} facilities".format(region, facilities.count()))
        return redirect('facilities:facility_settings')

    else:
            template = "facilities/facility-settings.html"
            return render(request, template)



# @login_required(login_url='login')
# def excel_uploaddd(request):
#     if request.method == 'POST' and request.FILES['excel_file']:
#         myfile = request.FILES['excel_file']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)

#         records = pe.get_records(file_name=settings.BASE_DIR+uploaded_file_url)
#         for record in records:
#             name = record['Name']
#             sex = record['sex']
#             age = record['age']

#             Profile(name=name, sex=sex,age=age).save()
#         return redirect('facilities:add_facility')
#     else:
#         return redirect('facilities:facilities')


