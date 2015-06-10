from django.shortcuts import render_to_response
from django.http import HttpResponse

# def index(request):
#    return HttpResponse('DPRR Homepage... Watch this space!')

def index(request):
	return render_to_response('homepage.html')

# def about(request):
#	return render_to_response('pages/about.html')