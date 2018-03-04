from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
# from .webservice.views import shop


def frontpage(request):
    return redirect('/shop/')

def error404(request):
    return HttpResponseNotFound('Custom 404 Not Found')

def error500(request):
    return HttpResponseServerError('Custom 500 Server Error')

def error403(request):
    return HttpResponseForbidden('Custom 403 error') 