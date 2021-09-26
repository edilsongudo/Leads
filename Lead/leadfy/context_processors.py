def domain(request):
    domain = request.META['HTTP_HOST'].replace('www.', '')
    return {'domain': domain}
