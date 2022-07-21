from django.http import HttpResponse
from django.shortcuts import render


def root(request):
    context = {}
    return render(request, 'root.html', context)
