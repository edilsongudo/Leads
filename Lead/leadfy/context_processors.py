def domain(request):
    domain = None
    if 'HTTP_HOST' in request.META:
        domain = request.META['HTTP_HOST']  # .replace('www.', '')
    return {'domain': domain}
