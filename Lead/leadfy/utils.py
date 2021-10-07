import uuid
from django.contrib.gis.geoip2 import GeoIP2
from urllib.parse import urlparse
from .writecss import writecss
import os
from django.conf import settings
import datetime
from django.db.models import Count
import folium
import pandas as pd


def context_dict(user, **kwargs):
    color1 = user.preferences.color1
    color2 = user.preferences.color2
    body_font_color = user.preferences.body_font_color
    font = user.preferences.font_family
    use_background_image = user.preferences.use_background_image
    mobileimage = user.preferences.background_image_mobile.url
    desktopimage = user.preferences.background_image_desktop.url
    background_image_brightness = user.preferences.background_image_brightness
    brightness_css_factor = background_image_brightness / 100
    primary_font_size = user.preferences.primary_font_size
    name_font_size = user.preferences.name_font_size
    border_radius = user.preferences.border_radius
    link_background_color = user.preferences.link_background_color
    link_border_color = user.preferences.link_border_color
    link_text_color = user.preferences.link_text_color
    font_family = user.preferences.font_family
    lastmodified = user.preferences.lastmodified

    if use_background_image:
        use_background_image = "true"
    else:
        use_background_image = "false"

    # CSS File creation is handled by a signal. This is just to guarantee that
    # the file will be created in case it does not exists
    if not os.path.isfile(
        os.path.join(
            settings.MEDIA_ROOT,
            f'customstylesheets/{user.username}.css')):
        writecss(user)

    data = {
        'user': user,
        'color1': color1,
        'color2': color2,
        'body_font_color': body_font_color,
        'font': font,
        'use_background_image': use_background_image,
        'mobileimage': mobileimage,
        'desktopimage': desktopimage,
        'brightness': background_image_brightness,
        'brightness_css_factor': brightness_css_factor,
        'primary_font_size': primary_font_size,
        'name_font_size': name_font_size,
        'border_radius': border_radius,
        'link_background_color': link_background_color,
        'link_border_color': link_border_color,
        'link_text_color': link_text_color,
        'font_family': font_family,
        'lastmodified': lastmodified
    }

    for k, v in kwargs.items():
        data[k] = v

    return data


def generate_ref_code():
    code = str(uuid.uuid4()).replace('-', '')[:5].lower()
    return code


def generate_netloc(url):
    netloc = urlparse(url).netloc
    return netloc


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon


def get_center_coordinates(latA, longA, latB=None, longB=None):
    cord = (latA, longA)
    if latB:
        cord = [(latA + latB) / 2, (longA + longB) / 2]
    return cord


def get_zoom(distance):
    if distance <= 100:
        return 8
    elif distance > 100 and distance <= 5000:
        return 4
    else:
        return 2


def set_http_referer(request, response, username):
    if not f'{username}_referer' in request.COOKIES:
        max_age = 60 * 5

        # it is important to set HTTP_REFERER TO EMPTY STRING
        # if its equal to None to avoid urllibe.urlparse returning EMPTY BYTES
        referer = request.META.get('HTTP_REFERER', "")

        referer_netloc = generate_netloc(referer)
        host = request.get_host()
        if referer_netloc == referer_netloc:
            referer = ""

        if referer != "":
            response.set_cookie(f'{username}_referer',
                                referer, max_age=max_age)
    else:
        referer = request.COOKIES.get(f'{username}_referer')
    print('REFERER: ', referer)
    return referer


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location(request):
    try:
        ip = get_ip(request)
        country, city, lat, lon = get_geo(ip)
        print(country, city)
        return {
            'country_name': country['country_name'],
            'country_code': country['country_code']}
    except Exception as e:
        print(e)
        return {'country_name': '', 'country_code': ''}


def contrast_gradient(color, color2):
    r1 = color[0]
    g1 = color[1]
    b1 = color[2]

    r2 = color2[0]
    g2 = color2[1]
    b2 = color2[2]

    luminance1 = (0.299 * r1 + 0.587 * g1 + 0.114 * b1) / 255
    luminance2 = (0.299 * r2 + 0.587 * g2 + 0.114 * b2) / 255

    if luminance1 > 0.75 and luminance2 > 0.75:
        font_color = 'rgba(0,0,0,1)'
    else:
        font_color = 'rgba(255, 255, 255, 1)'

    return font_color


def contrast_color(color):
    r = color[0]
    g = color[1]
    b = color[2]
    a = color[3]

    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

    if luminance > 0.5 and luminance > 0.5:
        font_color = 'rgba(0,0,0,1)'
    else:
        font_color = 'rgba(255, 255, 255, 1)'

    return font_color


def get_days(day1, day2, model, request):
    delta = day2 - day1
    list_of_days = []
    list_of_days2 = []
    for i in range(delta.days + 1):
        day = day1 + datetime.timedelta(days=i)
        pages_visits = model.objects.filter(
            page__user=request.user, time__date=day).count()
        list_of_days.append(pages_visits)
        list_of_days2.append(f'{day.strftime("%d/%m")}')
    return {'list_of_days': list_of_days, 'list_of_days2': list_of_days2}


def number_of_clicks(date1, date2, model, request):
    number_of_clicks = model.objects.filter(
        page__user=request.user,
        time__date__gte=date1,
        time__date__lte=date2).count()
    return number_of_clicks


def number_of_leads(date1, date2, model, request):
    number_of_leads = model.objects.filter(
        lead_from=request.user,
        date_submited__date__gte=date1,
        date_submited__date__lte=date2).count()
    return number_of_leads


def hours(date1, date2, model, request):
    hours = []
    labels = []
    for i in range(0, 24):
        pages_visits = model.objects.filter(
            page__user=request.user,
            time__date__gte=date1,
            time__date__lte=date2,
            time__hour=i)
        hours.append(len(pages_visits))
        labels.append(i)
    return {'hours': hours, 'labels': labels}


def get_referers(day1, day2, model, request):
    allpagevisitsorderedbyrefferer = model.objects.filter(
        page__user=request.user, time__date__gte=day1, time__date__lte=day2)
    allpagevisitsorderedbyrefferer = allpagevisitsorderedbyrefferer.values_list(
        'referer_main_domain').annotate(truck_count=Count('referer_main_domain')).order_by('-truck_count')
    allvisits = list(allpagevisitsorderedbyrefferer)
    channels = []
    visits = []
    for value in allvisits:
        channels.append(value[0])
        visits.append(value[1])

    return {'channels': channels, 'visits': visits}


def get_map(day1, day2, model, request):
    allpagevisitsorderedbylocation = model.objects.filter(
        page__user=request.user, time__date__gte=day1, time__date__lte=day2)

    allpagevisitsorderedbylocation = allpagevisitsorderedbylocation.values_list(
        'location', 'location_code').annotate(
        truck_count=Count('location')).order_by('-truck_count')

    df = pd.DataFrame(
        allpagevisitsorderedbylocation,
        columns=[
            'location',
            'location_code',
            'truck_count'])
    print(df)

    state_geo = 'geoip/custom.geo (1).json'
    m = folium.Map(location=[0, 0], zoom_start=0)
    folium.Choropleth(
        geo_data=state_geo,
        name='Choropleth',
        data=df,
        columns=[
            'location',
            'truck_count'],
        key_on="feature.properties.sovereignt",
        fill_color="YlGn",
        fill_opacity=0.5,
        line_opacity=0.2,
        legend_name="Links Visits").add_to(m)
    folium.LayerControl().add_to(m)

    m = m._repr_html_()

    return m


def get_user_agent(request):
    device_type = ''
    browser_type = ''
    browser_version = ''
    os_type = ''
    os_version = ''

    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"

    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string

    context = {
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version": os_version
    }

    return context
