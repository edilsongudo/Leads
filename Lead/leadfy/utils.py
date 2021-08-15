import uuid
from django.contrib.gis.geoip2 import GeoIP2
from urllib.parse import urlparse


def context_dict(user, **kwargs):
    color1 = user.preferences.color1
    color2 = user.preferences.color2
    body_font_color = user.preferences.body_font_color
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
        'body_font_color': body_font_color,
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
    if not 'referer' in request.COOKIES:
        max_age = 86400 * 14
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
