def context_dict(request=None, user=None, link=None, links=None, form=None):
    color1 = user.preferences.color1
    color2 = user.preferences.color2
    font = user.preferences.font_family
    use_background_image = user.preferences.use_background_image
    image = user.preferences.background_image.url
    background_image_brightness = user.preferences.background_image_brightness
    primary_font_size = user.preferences.primary_font_size
    name_font_size = user.preferences.name_font_size
    border_radius = user.preferences.border_radius
    link_background_color = user.preferences.link_background_color
    link_text_color = user.preferences.link_text_color

    if use_background_image:
        use_background_image = "true"
    else:
        use_background_image = "false"

    data = {
        'link': link,
        'links': links,
        'form': form,
        'user': user,
        'color1': color1,
        'color2': color2,
        'font': font,
        'use_background_image': use_background_image,
        'image': image,
        'brightness': background_image_brightness,
        'primary_font_size': primary_font_size,
        'name_font_size': name_font_size,
        'border_radius': border_radius,
        'link_background_color': link_background_color,
        'link_text_color': link_text_color,
    }

    return data


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
