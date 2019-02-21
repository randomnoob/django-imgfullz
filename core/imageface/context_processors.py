def site_name(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    return {'site_name': 'Hay Ho Site', 'site_url' : '/', 'site_mail': 'ngocbe2112@gmail.com'} 
