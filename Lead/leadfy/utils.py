import uuid
from django.contrib.gis.geoip2 import GeoIP2
from urllib.parse import urlparse

def context_dict(user, **kwargs):
    color1 = user.preferences.color1
    color2 = user.preferences.color2
    font = user.preferences.font_family
    use_background_image = user.preferences.use_background_image
    mobileimage = user.preferences.background_image_mobile.url
    desktopimage = user.preferences.background_image_desktop.url
    background_image_brightness = user.preferences.background_image_brightness
    primary_font_size = user.preferences.primary_font_size
    name_font_size = user.preferences.name_font_size
    border_radius = user.preferences.border_radius
    link_background_color = user.preferences.link_background_color
    link_text_color = user.preferences.link_text_color
    font_family = user.preferences.font_family

    if use_background_image:
        use_background_image = "true"
    else:
        use_background_image = "false"

    data = {
        'user': user,
        'color1': color1,
        'color2': color2,
        'font': font,
        'use_background_image': use_background_image,
        'mobileimage': mobileimage,
        'desktopimage': desktopimage,
        'brightness': background_image_brightness,
        'primary_font_size': primary_font_size,
        'name_font_size': name_font_size,
        'border_radius': border_radius,
        'link_background_color': link_background_color,
        'link_text_color': link_text_color,
        'font_family': font_family
    }

    for k, v in kwargs.items():
        data[k] = v

    return data


def generate_ref_code():
    code = str(uuid.uuid4()).replace('-', '')[:5]
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


def set_http_referer(request, response):
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    if not referer in request.COOKIES:
        max_age = 3600 * 24 * 90
        response.set_cookie('referer', referer, max_age=max_age)
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
        return country
    except Exception as e:
        print(e)
        return ''
