from django.shortcuts import render, HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
import geoip2.errors
from datetime import datetime

def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""

    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"
    
    message = ""
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    g = GeoIP2()
    
    #NOTE Following is band-aid fix for error "AddressNotFoundError at /. The address 127.0.0.1 is not in the database."
    try:
        location = g.city(ip)
    except geoip2.errors.AddressNotFoundError:
        mock_ip = "108.174.10.10"
        location = g.city(mock_ip) #use dummy ip then
        message = "(NNNOTE-> USING MOCK IP SINCE YOU ARE RUNNING THIS LOCALLY)"
        #print(message)
        
    location_country = location["country_name"]
    location_city = location["city"]

    context = {
        "message": message,
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version": os_version,
        "location_country": location_country,
        "location_city": location_city,
        "visit_time": datetime.now().strftime('%Y-%m-%d  %H:%M:%S'),
    }

    return render(request, "home.html", context)